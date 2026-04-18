from django.shortcuts import render
from categories.models import Category
from products.models import Product


def home(request):
    categories = Category.objects.prefetch_related('products').all()
    featured = Product.objects.filter(is_available=True).select_related('category')[:8]
    return render(request, 'home.html', {'categories': categories, 'featured': featured})
