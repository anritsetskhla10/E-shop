from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Category, Product


def home_view(request):
    products = Product.objects.filter(is_available=True).order_by('price')
    categories = (
        Category.objects
        .annotate(num_products=Count('products'))
        .filter(num_products__gt=0)
    )

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'shop/product_list.html', context)


def category_products_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.filter(is_available=True).order_by('price')

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'shop/category_products.html', context)


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})


def sale_products_view(request):
    products = Product.objects.filter(is_available=True, is_on_sale=True).order_by('price')
    return render(request, 'shop/sale_products.html', {'products': products})
