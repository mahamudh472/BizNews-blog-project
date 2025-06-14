from django.shortcuts import render, redirect
from blogs.models import Blog, Category
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator


categories = [i.name for i in Category.objects.all()]
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
    global categories
    four_blogs = Blog.objects.order_by('?')[0:4]
    context = {
        'four_blogs': four_blogs,
        'categories': categories,
    }
    return render(request, 'index.html', context)

def category(request):
    context = {
        'categories': {},
        'single_category': False
    }
    for cat in Category.objects.all():
        context['categories'][cat.name] = {
            'blogs': cat.blogs.all()[:2],
            'count': cat.blogs.count()
        }
    context['categories'] = dict(sorted(context['categories'].items(), key=lambda item: item[1]['count'], reverse=True))
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

    context = {
        'blog' : blog_object
    }
    return render(request, 'blog.html', context)

def contact(request):
    return render(request, 'contact.html')