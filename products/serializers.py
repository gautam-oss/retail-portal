from rest_framework import serializers
from .models import Product
from categories.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    price_with_tax = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'description', 'cost', 'tax_percent',
            'image', 'stock', 'category', 'category_detail',
            'is_available', 'price_with_tax', 'created_at',
        )
        read_only_fields = ('id', 'created_at')

    def get_price_with_tax(self, obj):
        return float(obj.price_with_tax())


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'stock')
