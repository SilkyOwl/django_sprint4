from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Post, Category
from config import POSTS_ON_PAGE


def get_published_posts(post_id=None):
    """Returns only published posts."""
    queryset = Post.objects.filter(
        Q(pub_date__lte=timezone.now())
        & Q(is_published=True)
        & Q(category__is_published=True)
    )
    if post_id is not None:
        queryset = queryset.filter(pk=post_id)
    return queryset


def index(request: HttpRequest) -> HttpResponse:
    """Renders the index page with a list of posts."""
    template = 'blog/index.html'
    post_list = get_published_posts()[:POSTS_ON_PAGE]
    context = {'post_list': post_list}
    return render(request, template, context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Renders a list of blog posts in a specific category."""
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    category_posts = get_published_posts().filter(category=category)
    context = {
        'category': category,
        'post_list': category_posts
    }
    return render(request, template, context)


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    """Renders the detail page for a specific post."""
    template = 'blog/detail.html'
    post = get_published_posts(id).first()
    if post is None:
        raise Http404("Страница не найдена")
    context = {
        'post': post,
        'category': post.category,
        'post_title': post.title,
    }
    return render(request, template, context)


def profile(request: HttpRequest, username=None) -> HttpResponse:
    template = 'blog/profile.html'
    # TODO: debug why nonexistant username does not show desired custom 404 page?!
    user = get_object_or_404(User, username=username)
    print(user)
    return render(request, template)



# from django.views.generic import (
#     CreateView, DeleteView, DetailView, ListView, UpdateView
# )
# from django.urls import reverse_lazy
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.exceptions import PermissionDenied
# from django.shortcuts import get_object_or_404, redirect


# from .forms import PostForm 
# from .models import Post
# # from .utils import calculate_birthday_countdown
# from .views import index, post_detail, category_posts


# @login_required
# def simple_view(request):
#     return HttpResponse('Страница для залогиненных пользователей!')


# @login_required
# def add_comment(request, pk):
#     blog = get_object_or_404(Blog, pk=pk)
#     form = CommentForm(request.POST)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.author = request.user
#         comment.blog = blog
#         comment.save()
#     return redirect('blog:detail', pk=pk)


# class PostListView(ListView):
#     model = Post
#     # #queryset = Post.objects.prefetch_related(
#     #     'tags'
#     # ).select_related('author')
#     ordering = 'id'
#     paginate_by = 10


# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     form_class = PostForm

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


# class PostUpdateView(LoginRequiredMixin, UpdateView):
#     model = Post
#     form_class = PostForm

#     def dispatch(self, request, *args, **kwargs):
#         instance = get_object_or_404(Post, pk=kwargs['pk'])
#         if instance.author != request.user:
#             raise PermissionDenied
#         return super().dispatch(request, *args, **kwargs)


# class PostDeleteView(LoginRequiredMixin, DeleteView):
#     model = Post
#     success_url = reverse_lazy('post:list')

#     def dispatch(self, request, *args, **kwargs):
#         instance = get_object_or_404(Post, pk=kwargs['pk'])
#         if instance.author != request.user:
#             raise PermissionDenied
#         return super().dispatch(request, *args, **kwargs)


# class PostDetailView(DetailView):
#     model = Post

#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['birthday_countdown'] = calculate_birthday_countdown(
#     #         self.object.birthday
#     #     )
#     #     context['form'] = CongratulationForm()
#     #     context['congratulations'] = (
#     #         self.object.congratulations.select_related('author')
#     #     )
#     #     return context
