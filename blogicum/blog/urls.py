from django.urls import path
from .views import index, post_detail, category_posts, profile

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('posts/<int:id>/', post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', category_posts,
         name='category_posts'),
    path('profile/<username>/', profile, name='profile'),
]

# from django.urls import path

# from . import views

# app_name = 'blog'

# urlpatterns = [
#     path('create/', views.PostCreateView.as_view(), name='create'),
#     path('list/', views.PostListView.as_view(), name='list'),
#     path('<int:pk>/', views.PostDetailView.as_view(), name='detail'),
#     path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit'),
#     path('<int:pk>/delete/',
#          views.PostDeleteView.as_view(), name='delete'),
#     path('<int:pk>/comment/', views.add_comment, name='add_comment'),
#     path('login_only/', views.simple_view),
# ]
