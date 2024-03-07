from .models import Comment, Post
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone


class PostsEditMixin:
    model = Post
    template_name = "blog/create.html"
    queryset = Post.objects.select_related(
        "author",
        "location",
        "category"
    )


class CommentEditMixin:
    model = Comment
    pk_url_kwarg = "comment_pk"
    template_name = "blog/comment.html"


class SuccessUrlMixin:
    def get_success_url(self):
        return reverse("blog:post_detail",
                       kwargs={"pk": self.kwargs["pk"]})


class VisiblePostsMixin:
    @staticmethod
    def visible_posts_queryset():
        filters = (
            Q(is_published=True)
            & Q(category__is_published=True)
            & Q(pub_date__lte=timezone.now())
        )
        return Post.post_list.filter(filters)


class PostDetailsMixin:
    @staticmethod
    def post_details_queryset(author):
        if author.is_authenticated:
            filters = (
                Q(author=author)
                | Q(is_published=True)
                & Q(category__is_published=True)
            )
        else:
            filters = (
                Q(is_published=True)
                & Q(category__is_published=True)
            )
        return Post.post_list.filter(filters).prefetch_related("comments")
