from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'logo', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
