from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path(
        "",
        views.BlogIndexListView.as_view(),
        name="index"
    ),
    path(
        "posts/<int:pk>/",
        views.PostDetailView.as_view(),
        name="post_detail"
    ),
    path(
        "category/<slug:category_slug>/",
        views.BlogCategoryListView.as_view(),
        name="category_posts",
    ),
    path(
        "profile/<str:username>/",
        views.AuthorProfileListView.as_view(),
        name="profile",
    ),
    path(
        "posts/create/",
        views.PostCreateView.as_view(),
        name="create_post"
    ),
    path(
        "posts/<int:pk>/edit/",
        views.PostUpdateView.as_view(),
        name="edit_post",
    ),
    path(
        "posts/<int:pk>/delete/",
        views.PostDeleteView.as_view(),
        name="delete_post",
    ),
    path(
        "posts/<int:pk>/comment/",
        views.CommentCreateView.as_view(),
        name="add_comment",
    ),
    path(
        "posts/<int:pk>/edit_comment/<int:comment_pk>/",
        views.CommentUpdateView.as_view(),
        name="edit_comment",
    ),
    path(
        "posts/<int:pk>/delete_comment/<int:comment_pk>/",
        views.CommentDeleteView.as_view(),
        name="delete_comment",
    ),
    path(
        "accounts/profile/",
        views.ProfileView.as_view(),
        name='user_profile'
    ),
    path(
        "edit_profile/",
        views.EditProfileView.as_view(),
        name="edit_profile"),
]
