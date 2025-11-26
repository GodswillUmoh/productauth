from django.urls import path
from . import views

app_name = 'blog'  # This registers the namespace

urlpatterns = [
    path('list/', views.blog_list, name= 'list'),  # List of all blog posts
    # Optional: path('<int:post_id>/', views.blog_detail, name='detail'),  # Only add if you implement detail page
]
