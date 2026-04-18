from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('blog/new/', views.create_blog, name='create_blog'),
    path('blog/<int:pk>/update/', views.update_blog, name='update_blog'),
    path('blog/<int:pk>/delete/', views.delete_blog, name='delete_blog'),
    path('history/', views.blog_history, name='blog_history'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('comment/<int:pk>/', views.add_comment, name='add_comment'),
]
