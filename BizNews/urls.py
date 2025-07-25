"""
URL configuration for BizNews project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('search', views.search, name="search"),
    path('category', views.category, name="category"),
    path('category/<str:category>', views.category_blogs, name="category_blogs"),
    path('blog/<slug>', views.blog, name="blog"),
    path('single_news', views.single_news, name="single_news"),
    path('contact', views.contact, name="contact"),
    path('login', views.Login, name="login"),
    path('logout', views.Logout, name="logout"),
    path('ckeditor5/', include('django_ckeditor_5.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
