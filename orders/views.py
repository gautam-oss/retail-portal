from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.models import Product
from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer


# --- Template Views ---

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'orders/list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})


@login_required
def order_create(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('product_ids[]')
        quantities = request.POST.getlist('quantities[]')
        if not product_ids:
            messages.error(request, 'No items selected.')
            return redirect('product-list')

        order = Order.objects.create(user=request.user, total=0)
        total = 0
        for pid, qty in zip(product_ids, quantities):
            try:
                product = Product.objects.get(pk=pid, is_available=True)
                qty = int(qty)
                subtotal = product.price_with_tax() * qty
                OrderItem.objects.create(order=order, product=product, quantity=qty, subtotal=subtotal)
                total += subtotal
            except (Product.DoesNotExist, ValueError):
                continue
        order.total = total
        order.save()
        messages.success(request, f'Order #{order.pk} placed successfully!')
        return redirect('order-detail', pk=order.pk)
    return redirect('product-list')


@login_required
def order_reorder(request, pk):
    original = get_object_or_404(Order, pk=pk, user=request.user)
    new_order = Order.objects.create(user=request.user, total=original.total)
    for item in original.items.all():
        OrderItem.objects.create(
            order=new_order,
            product=item.product,
            quantity=item.quantity,
            subtotal=item.subtotal,
        )
    messages.success(request, f'Re-ordered as Order #{new_order.pk}.')
    return redirect('order-detail', pk=new_order.pk)


# --- API Views ---

class OrderListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = Order.objects.create(user=request.user, total=0)
        total = 0
        for item_data in serializer.validated_data['items']:
            try:
                product = Product.objects.get(pk=item_data['product'], is_available=True)
                qty = item_data['quantity']
                subtotal = product.price_with_tax() * qty
                OrderItem.objects.create(order=order, product=product, quantity=qty, subtotal=subtotal)
                total += subtotal
            except Product.DoesNotExist:
                continue
        order.total = total
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def order_reorder_api(request, pk):
    original = get_object_or_404(Order, pk=pk, user=request.user)
    new_order = Order.objects.create(user=request.user, total=original.total)
    for item in original.items.all():
        OrderItem.objects.create(
            order=new_order,
            product=item.product,
            quantity=item.quantity,
            subtotal=item.subtotal,
        )
    return Response(OrderSerializer(new_order).data, status=status.HTTP_201_CREATED)
