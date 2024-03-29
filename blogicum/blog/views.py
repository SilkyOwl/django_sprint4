from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from .forms import (
    CreateCommentForm,
    CreatePostForm,
    UserForm,
)
from .models import Category, Comment, Post, User
from .mixins import (
    CommentEditMixin,
    PostsEditMixin,
    SuccessUrlMixin,
    VisiblePostsMixin,
    PostDetailsMixin
)


PAGINATED_BY = 10


class PostCreateView(PostsEditMixin, LoginRequiredMixin, CreateView):
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            "blog:profile",
            kwargs={"username": self.request.user.username},
        )


class PostDeleteView(PostsEditMixin, LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy("blog:index")

    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        if self.request.user != post.author:
            return redirect("blog:index")

        return super().delete(request, *args, **kwargs)


class PostUpdateView(PostsEditMixin, LoginRequiredMixin, UpdateView):
    form_class = CreatePostForm

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        if self.request.user != post.author:
            return redirect("blog:post_detail", pk=self.kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(
    LoginRequiredMixin,
    SuccessUrlMixin,
    CreateView
):
    model = Comment
    form_class = CreateCommentForm

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["pk"])
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentDeleteView(
    CommentEditMixin,
    LoginRequiredMixin,
    SuccessUrlMixin,
    DeleteView
):

    def delete(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs["comment_pk"])
        if self.request.user != comment.author:
            return redirect("blog:post_detail", pk=self.kwargs["pk"])
        return super().delete(request, *args, **kwargs)


class CommentUpdateView(
    CommentEditMixin,
    LoginRequiredMixin,
    SuccessUrlMixin,
    UpdateView
):
    form_class = CreateCommentForm

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs["comment_pk"])
        if self.request.user != comment.author:
            return redirect("blog:post_detail", pk=self.kwargs["pk"])

        return super().dispatch(request, *args, **kwargs)


class AuthorProfileListView(VisiblePostsMixin, ListView):
    model = Post
    template_name = "blog/profile.html"
    paginate_by = PAGINATED_BY

    def get_queryset(self):
        if self.request.user.username == self.kwargs["username"]:
            return (
                self.request.user.posts.select_related(
                    "category",
                    "author",
                    "location",
                )
                .all()
                .annotate(comment_count=Count("comments"))
                .order_by('-pub_date')
            )

        return (
            super()
            .visible_posts_queryset()
            .filter(author__username=self.kwargs["username"])
            .annotate(comment_count=Count("comments"))
            .order_by('-pub_date')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(
            User, username=self.kwargs["username"]
        )
        return context


class BlogIndexListView(VisiblePostsMixin, ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "post_list"
    paginate_by = PAGINATED_BY

    def get_queryset(self):
        return super().visible_posts_queryset().annotate(
            comment_count=Count("comments"))


class BlogCategoryListView(VisiblePostsMixin, ListView):
    model = Post
    template_name = "blog/category.html"
    context_object_name = "post_list"
    paginate_by = PAGINATED_BY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(
            Category, slug=self.kwargs["category_slug"], is_published=True
        )
        return context

    def get_queryset(self):
        return (
            super()
            .visible_posts_queryset()
            .filter(category__slug=self.kwargs["category_slug"])
            .annotate(comment_count=Count("comments"))
        )


class PostDetailView(DetailView, PostDetailsMixin):
    model = Post
    template_name = "blog/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CreateCommentForm()
        context["comments"] = (
            self.object.comments.prefetch_related("author").all()
        )
        return context

    def get_queryset(self):
        return (
            super().post_details_queryset(author=self.request.user)
        )


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        template_name = "blog/profile.html"
        if request.user.is_authenticated:
            user = request.user
            posts = Post.objects.filter(author=user)
            context = {
                'user': user,
                'posts': posts,
            }
            return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        template_name = "blog/profile.html"
        if request.user.is_authenticated:
            user = request.user
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("blog:profile")
            context = {
                'user': user,
                'form': form,
            }
            return render(request, template_name, context)


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = "blog/user.html"
    success_url = reverse_lazy("blog:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )
