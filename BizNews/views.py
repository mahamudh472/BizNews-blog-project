from django.shortcuts import render, redirect
from blogs.models import Blog 
from django.contrib.auth import authenticate, login, logout

categories = [i[0] for i in Blog.categories]
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

def catagory(request):
    return render(request, 'category.html')

def blog(request, slug):
    blog_object = Blog.objects.get(slug = slug)
    
    context = {
        'blog' : blog_object
    }
    return render(request, 'blog.html', context)

def contact(request):
    return render(request, 'contact.html')