from .models import Category

def categories(request):
    """
    Context processor to add categories to the context.
    """
    categories = Category.objects.all()
    return {'categories': categories}