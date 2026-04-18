from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'cost', 'stock', 'is_available', 'created_at')
    list_filter = ('category', 'is_available')
    search_fields = ('title', 'description')
    list_editable = ('stock', 'is_available')
