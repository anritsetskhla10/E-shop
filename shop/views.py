from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .models import Category, Product
from .forms import ProductForm


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
    categories = (
        Category.objects
        .annotate(num_products=Count('products'))
        .filter(num_products__gt=0)
    )

    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'shop/category_products.html', context)


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = (
        Category.objects
        .annotate(num_products=Count('products'))
        .filter(num_products__gt=0)
    )
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'categories': categories,
    })


def sale_products_view(request):
    products = Product.objects.filter(is_available=True, is_on_sale=True).order_by('price')
    categories = (
        Category.objects
        .annotate(num_products=Count('products'))
        .filter(num_products__gt=0)
    )
    return render(request, 'shop/sale_products.html', {
        'products': products,
        'categories': categories,
    })


def shop_view(request):
    products = Product.objects.filter(is_available=True).order_by('price')
    categories = (
        Category.objects
        .annotate(num_products=Count('products'))
        .filter(num_products__gt=0)
    )
    return render(request, 'shop/shop.html', {
        'products': products,
        'categories': categories,
    })


def cart_view(request):
    categories = (
        Category.objects
        .annotate(num_products=Count('products'))
        .filter(num_products__gt=0)
    )
    return render(request, 'shop/cart.html', {'categories': categories})


def checkout_view(request):
    categories = (
        Category.objects
        .annotate(num_products=Count('products'))
        .filter(num_products__gt=0)
    )
    return render(request, 'shop/cheackout.html', {'categories': categories})


def contact_view(request):
    categories = (
        Category.objects
        .annotate(num_products=Count('products'))
        .filter(num_products__gt=0)
    )
    return render(request, 'shop/contact.html', {'categories': categories})


def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('shop:product_detail', product_id=product.id)
    else:
        form = ProductForm()

    categories = (
        Category.objects
        .annotate(num_products=Count('products'))
        .filter(num_products__gt=0)
    )
    return render(request, 'shop/product_form.html', {
        'form': form,
        'title': 'Add New Product',
        'button_text': 'Create Product',
        'categories': categories,
    })


def product_update_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop:product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)

    categories = (
        Category.objects
        .annotate(num_products=Count('products'))
        .filter(num_products__gt=0)
    )
    return render(request, 'shop/product_form.html', {
        'form': form,
        'product': product,
        'title': f'Edit Product: {product.name}',
        'button_text': 'Save Changes',
        'categories': categories,
    })


def product_delete_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('shop:home')

    categories = (
        Category.objects
        .annotate(num_products=Count('products'))
        .filter(num_products__gt=0)
    )
    return render(request, 'shop/product_confirm_delete.html', {
        'product': product,
        'categories': categories,
    })