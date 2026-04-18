from django.shortcuts import render
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from products.models import Product
from categories.models import Category


def search_results(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.none()
    if query:
        products = (
            Product.objects
            .annotate(
                similarity=Greatest(
                    TrigramSimilarity('title', query),
                    TrigramSimilarity('description', query),
                    TrigramSimilarity('category__name', query),
                )
            )
            .filter(
                Q(similarity__gte=0.1) |
                Q(title__icontains=query) |
                Q(category__name__icontains=query),
                is_available=True,
            )
            .select_related('category')
            .order_by('-similarity')
            .distinct()
        )
    categories = Category.objects.all()
    return render(request, 'search/results.html', {
        'query': query,
        'products': products,
        'categories': categories,
    })
