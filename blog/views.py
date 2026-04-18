from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BlogPost, Profile, Comment, Like
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, BlogPostForm, CommentForm
from django.http import JsonResponse

def index(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    comment_form = CommentForm()
    return render(request, 'blog/index.html', {'posts': posts, 'comment_form': comment_form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('index')
    else:
        form = BlogPostForm()
    return render(request, 'blog/blog_form.html', {'form': form, 'title': 'Create Blog'})

@login_required
def update_blog(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You are not authorized to edit this post.')
        return redirect('index')
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('blog_history')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/blog_form.html', {'form': form, 'title': 'Update Blog'})

@login_required
def delete_blog(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You are not authorized to delete this post.')
        return redirect('index')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('blog_history')
    return render(request, 'blog/blog_confirm_delete.html', {'post': post})

@login_required
def blog_history(request):
    posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/blog_history.html', {'posts': posts})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'blog/profile.html', {'u_form': u_form, 'p_form': p_form})

@login_required
def like_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    like_qs = Like.objects.filter(post=post, user=request.user)
    if like_qs.exists():
        like_qs.delete()
        liked = False
    else:
        Like.objects.create(post=post, user=request.user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'like_count': post.likes.count()
    })

@login_required
def add_comment(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('index')
    return redirect('index')
