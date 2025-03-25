from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import User, BlogPost, Comment, Category
from django.utils import timezone
from datetime import timedelta
from django.utils.text import slugify

# Create your views here.

def home(request):
    # Get latest 3 blog posts
    latest_posts = BlogPost.objects.all()[:3]
    
    # Get active bloggers (users who have posted in the last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    active_bloggers = User.objects.filter(
        blog_posts__created_at__gte=thirty_days_ago
    ).distinct().order_by('-blog_posts__created_at')[:5]
    
    # Get categories for sidebar
    categories = Category.objects.all()
    
    return render(request, 'index.html', {
        'latest_posts': latest_posts,
        'active_bloggers': active_bloggers,
        'categories': categories
    })

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
        
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, full_name=full_name, password=password)
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('home')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Set session variable to show welcome toast
            request.session['show_welcome_toast'] = True
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

@require_POST
def clear_welcome_toast(request):
    if 'show_welcome_toast' in request.session:
        del request.session['show_welcome_toast']
    return JsonResponse({'status': 'success'})

def blog_list(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    
    posts = BlogPost.objects.all()
    
    # Filter by category if provided
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(categories=category)
    
    # Filter by search query if provided
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    # Get categories for sidebar
    categories = Category.objects.all()
    
    return render(request, 'blog_list.html', {
        'posts': posts,
        'categories': categories, 
        'current_category': category_slug,
        'search_query': search_query
    })

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    categories = Category.objects.all()
    
    # Get comments for the post with most recent first
    comments = post.comments.all().order_by('-created_at')
    
    return render(request, 'blog_detail.html', {
        'post': post,
        'categories': categories,
        'comments': comments
    })

@login_required
def create_post(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_ids = request.POST.getlist('categories')
        featured_image = request.FILES.get('featured_image')
        
        if not title or not content:
            messages.error(request, 'Title and content are required')
            return render(request, 'post_form.html', {'categories': categories})
        
        # Create post
        post = BlogPost.objects.create(
            title=title,
            content=content,
            author=request.user
        )
        
        # Add featured image if provided
        if featured_image:
            post.featured_image = featured_image
            post.save()
        
        # Add categories
        if category_ids:
            post.categories.set(category_ids)
        
        messages.success(request, 'Post created successfully!')
        return redirect('blog_detail', post_id=post.id)
    
    return render(request, 'post_form.html', {'categories': categories})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    # Check if user is the author
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this post")
        return redirect('blog_detail', post_id=post.id)
    
    categories = Category.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_ids = request.POST.getlist('categories')
        featured_image = request.FILES.get('featured_image')
        
        if not title or not content:
            messages.error(request, 'Title and content are required')
            return render(request, 'post_form.html', {'post': post, 'categories': categories})
        
        # Update post
        post.title = title
        post.content = content
        
        # Update featured image if provided
        if featured_image:
            post.featured_image = featured_image
        
        post.save()
        
        # Update categories
        post.categories.set(category_ids)
        
        messages.success(request, 'Post updated successfully!')
        return redirect('blog_detail', post_id=post.id)
    
    return render(request, 'post_form.html', {'post': post, 'categories': categories})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    # Check if user is the author
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, "You don't have permission to delete this post")
        return redirect('blog_detail', post_id=post.id)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('blog_list')
    
    return render(request, 'post_confirm_delete.html', {'post': post})

def author_detail(request, author_id):
    author = get_object_or_404(User, id=author_id)
    posts = BlogPost.objects.filter(author=author)
    return render(request, 'author_detail.html', {'author': author, 'posts': posts})

def blogger_detail(request, author_id):
    author = get_object_or_404(User, id=author_id)
    posts = BlogPost.objects.filter(author=author).order_by('-created_at')
    return render(request, 'blogger_detail.html', {
        'author': author,
        'posts': posts
    })

def blogger_list(request):
    # Get all users who have published at least one blog post
    bloggers = User.objects.filter(blog_posts__isnull=False).distinct().order_by('username')
    return render(request, 'blogger_list.html', {'bloggers': bloggers})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(categories=category)
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, 'category_detail.html', {
        'category': category,
        'posts': posts
    })

@login_required
def create_category(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to create categories")
        return redirect('category_list')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        if not name:
            messages.error(request, 'Category name is required')
            return render(request, 'category_form.html')
        
        # Create slug from name
        slug = slugify(name)
        
        # Check if slug already exists
        if Category.objects.filter(slug=slug).exists():
            messages.error(request, 'A category with this name already exists')
            return render(request, 'category_form.html')
        
        # Create category
        category = Category.objects.create(
            name=name,
            slug=slug,
            description=description
        )
        
        messages.success(request, 'Category created successfully!')
        return redirect('category_detail', slug=category.slug)
    
    return render(request, 'category_form.html')

def search(request):
    query = request.GET.get('q', '')
    
    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct()
        
        # Pagination
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
    else:
        posts = BlogPost.objects.none()
    
    return render(request, 'search_results.html', {
        'posts': posts,
        'query': query
    })

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    content = request.POST.get('content')
    
    if not content:
        messages.error(request, 'Comment cannot be empty')
        return redirect('blog_detail', post_id=post.id)
    
    Comment.objects.create(
        content=content,
        author=request.user,
        post=post
    )
    
    messages.success(request, 'Comment added successfully!')
    return redirect('blog_detail', post_id=post.id)
