from django.shortcuts import render, redirect
from blogs.models import Blog, Category, Comment, BlogView
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from blogs.forms import CommentForm, AuthenticatedCommentForm
from django.db.models import Prefetch



def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
    if request.user.is_authenticated:
        return redirect('index')
    else:
        return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('index')

def index(request):
    four_blogs = Blog.objects.order_by('?')[0:4]
    context = {
        'four_blogs': four_blogs,
    }
    return render(request, 'index.html', context)

def search(request):
    query = request.GET.get('q')
    search_results = Blog.objects.filter(title__icontains=query)
    if not search_results:
        search_results = Blog.objects.none()
    if not query:
        search_results = Blog.objects.all()
    context = {
        'search_results': search_results,
        'query': query
    }
    return render(request, 'search_result.html', context)

def category(request):
    categories = Category.objects.prefetch_related(
        Prefetch('blogs', queryset=Blog.objects.all(), to_attr='all_blogs')
    )

    context = {
        'categories': {},
        'single_category': False
    }

    for cat in categories:
        sorted_blogs = sorted(cat.all_blogs, key=lambda x: x.created_at, reverse=True)[:2]
        context['categories'][cat.name] = {
            'blogs': sorted_blogs,
            'count': len(cat.all_blogs)
        }

    context['categories'] = dict(sorted(
        context['categories'].items(),
        key=lambda item: item[1]['count'],
        reverse=True
    ))

    return render(request, 'category.html', context)


def category_blogs(request, category):
    category_object = Category.objects.get(name=category)
    blogs = category_object.blogs.all()
    paginator = Paginator(blogs, 10)  # Show 5 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categories':{
            category_object: {
                'count': category_object.blogs.count(),
                'blogs': page_obj
            }
        },
        'single_category': True

    }
    return render(request, 'category.html', context)
    

def blog(request, slug):
    blog_object = Blog.objects.get(slug=slug)
    if request.method == "POST":
        form = AuthenticatedCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog_object
            if request.user.is_authenticated:
                comment.user = request.user
            else:
                comment.name = request.POST.get('name')
                comment.email = request.POST.get('email')
                comment.website = request.POST.get('website')
            comment.save()
            return redirect('blog', slug=slug)
        
    if request.user.is_authenticated:
        # Check if the user has already viewed the blog
        if not BlogView.objects.filter(blog=blog_object, user=request.user).exists():
            # Create a new BlogView entry
            BlogView.objects.create(blog=blog_object, user=request.user)
            # Increment the view count
            blog_object.views = BlogView.objects.filter(blog=blog_object).count()
            blog_object.views += 1
            blog_object.save()
        form = AuthenticatedCommentForm()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
        # Check if the session has already viewed the blog
        if not BlogView.objects.filter(blog=blog_object, session_key=session_key).exists():
            # Create a new BlogView entry
            BlogView.objects.create(blog=blog_object, session_key=session_key)
            blog_object.views = BlogView.objects.filter(blog=blog_object).count()
            blog_object.views += 1
            blog_object.save()
        form = CommentForm()


    context = {
        'blog' : blog_object,
        'form': form
    }
    return render(request, 'blog.html', context)

def contact(request):
    return render(request, 'contact.html')

def single_news(request):
    blog_object = Blog.objects.order_by('?').first()
    if not blog_object:
        return redirect('index')  # Redirect to index if no blogs are available
    return redirect('blog', slug=blog_object.slug)  # Redirect to the single blog page