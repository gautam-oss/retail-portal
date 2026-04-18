from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'cost', 'tax_percent', 'image', 'stock', 'category', 'is_available')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('stock',)
