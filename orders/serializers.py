from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_detail', 'quantity', 'subtotal')
        read_only_fields = ('subtotal',)


class OrderItemCreateSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'username', 'status', 'total', 'items', 'created_at', 'updated_at')
        read_only_fields = ('id', 'total', 'created_at', 'updated_at', 'username')


class CreateOrderSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(many=True)
