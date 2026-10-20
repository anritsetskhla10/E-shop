from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from .forms import ProductForm
from .models import Category, Product


# დამხმარე ფუნქცია
def get_annotated_categories():
    return (
        Category.objects.annotate(num_products=Count('products'))
        .filter(num_products__gt=0)
    )


class HomeView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_available=True).order_by('price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_annotated_categories()
        return context


class ShopView(ListView):
    model = Product
    template_name = 'shop/shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_available=True).order_by('price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_annotated_categories()
        return context


class CategoryProductsView(ListView):
    model = Product
    template_name = 'shop/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return self.category.products.filter(is_available=True).order_by('price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = get_annotated_categories()
        return context


class SaleProductsView(ListView):
    model = Product
    template_name = 'shop/sale_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_available=True, is_on_sale=True).order_by('price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_annotated_categories()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_annotated_categories()
        return context


class CartView(TemplateView):
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_annotated_categories()
        return context


class CheckoutView(TemplateView):
    template_name = 'shop/cheackout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_annotated_categories()
        return context


class ContactView(TemplateView):
    template_name = 'shop/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_annotated_categories()
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Product'
        context['button_text'] = 'Create Product'
        context['categories'] = get_annotated_categories()
        return context

    def get_success_url(self):
        return reverse('shop:product_detail', kwargs={'product_id': self.object.id})



def product_update_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop:product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'title': f'Edit Product: {product.name}',
        'button_text': 'Save Changes',
        'categories': get_annotated_categories(),
    }
    return render(request, 'shop/product_form.html', context)


def product_delete_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('shop:home')

    context = {
        'product': product,
        'categories': get_annotated_categories(),
    }
    return render(request, 'shop/product_confirm_delete.html', context)