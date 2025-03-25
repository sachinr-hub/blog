from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('clear-welcome-toast/', views.clear_welcome_toast, name='clear_welcome_toast'),
    
    # Blog Posts
    path('blog/blogs/', views.blog_list, name='blog_list'),
    path('blog/blogs/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('blog/create/', views.create_post, name='create_post'),
    path('blog/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('blog/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    
    # Comments
    path('blog/blogs/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    
    # Bloggers
    path('blog/bloggers/', views.blogger_list, name='blogger_list'),
    path('blog/bloggers/<int:author_id>/', views.blogger_detail, name='blogger_detail'),
    
    # Categories
    path('blog/categories/', views.category_list, name='category_list'),
    path('blog/categories/<slug:slug>/', views.category_detail, name='category_detail'),
    path('blog/categories/create/', views.create_category, name='create_category'),
    
    # Search
    path('search/', views.search, name='search'),
] 