from .models import Category, Blog

def categories(request):
    """
    Context processor to add categories to the context.
    """
    categories = Category.objects.all()
    return {'categories_list': categories}

def trending_blogs(request):
    """
    Context processor to add trending blogs to the context.
    """
    trending_blogs = Blog.objects.order_by('-views')[:5]  # Assuming 'views' is a field in Blog model
    return {'trending_blogs': trending_blogs}