from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'description',
            'price',
            'is_on_sale',
            'is_available',
        ]
        labels = {
            'category': 'Category',
            'name': 'Product Name',
            'description': 'Description',
            'price': 'Price',
            'is_on_sale': 'On Sale',
            'is_available': 'Available in Stock',
        }
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter detailed description',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00',
            }),
            'is_on_sale': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }