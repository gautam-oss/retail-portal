from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from categories.models import Category
from .models import Product
from .forms import ProductForm, StockUpdateForm
from .serializers import ProductSerializer, StockSerializer


def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin_user():
            messages.error(request, 'Admin access required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


# --- Template Views ---

def product_list(request):
    qs = Product.objects.filter(is_available=True).select_related('category')
    category_id = request.GET.get('category')
    if category_id:
        qs = qs.filter(category_id=category_id)
    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page', 1))
    categories = Category.objects.all()
    return render(request, 'products/list.html', {
        'page_obj': page,
        'categories': categories,
        'selected_category': category_id,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related = Product.objects.filter(category=product.category, is_available=True).exclude(pk=pk)[:4]
    return render(request, 'products/detail.html', {'product': product, 'related': related})


@admin_required
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Product created.')
        return redirect('product-list')
    return render(request, 'products/form.html', {'form': form, 'title': 'Add Product'})


@admin_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Product updated.')
        return redirect('product-detail', pk=pk)
    return render(request, 'products/form.html', {'form': form, 'title': 'Edit Product'})


@admin_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted.')
        return redirect('product-list')
    return render(request, 'products/confirm_delete.html', {'object': product})


@admin_required
def stock_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = StockUpdateForm(request.POST or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Stock updated.')
        return redirect('product-detail', pk=pk)
    return render(request, 'products/stock_form.html', {'form': form, 'product': product})


# --- API ViewSet ---

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = Product.objects.select_related('category')
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        if category:
            qs = qs.filter(category_id=category)
        if search:
            qs = qs.filter(title__icontains=search)
        return qs

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAdminUser()]

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def stock(self, request, pk=None):
        product = self.get_object()
        serializer = StockSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
