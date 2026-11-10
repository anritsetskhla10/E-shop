from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
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

class ProductFilterMixin:
    paginate_by = 6

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)

        #  ძებნა სახელში ან აღწერაში
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # ფილტრაცია კატეგორიით
        category_id = self.request.GET.get('category', '').strip()
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # ფილტრაცია მინიმალური ფასით
        min_price = self.request.GET.get('min_price', '').strip()
        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass

        # ფილტრაცია მაქსიმალური ფასით
        max_price = self.request.GET.get('max_price', '').strip()
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass

        # ფილტრაცია: მხოლოდ ფასდაკლებული პროდუქტები
        on_sale = self.request.GET.get('on_sale', '').strip()
        if on_sale == 'true':
            queryset = queryset.filter(is_on_sale=True)

        # სორტირება
        sort_by = self.request.GET.get('sort', '').strip()
        sort_options = {
            'price_asc': 'price',
            'price_desc': '-price',
            'newest': '-id',
            'name_asc': 'name',
            'name_desc': '-name',
        }
        order_field = sort_options.get(sort_by, 'price')
        queryset = queryset.order_by(order_field)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_annotated_categories()

        context['current_q'] = self.request.GET.get('q', '').strip()
        context['current_category'] = self.request.GET.get('category', '').strip()
        context['current_min_price'] = self.request.GET.get('min_price', '').strip()
        context['current_max_price'] = self.request.GET.get('max_price', '').strip()
        context['current_on_sale'] = self.request.GET.get('on_sale', '').strip()
        context['current_sort'] = self.request.GET.get('sort', '').strip()

        get_params = self.request.GET.copy()
        if 'page' in get_params:
            del get_params['page']
        context['preserved_params'] = get_params.urlencode()

        return context


class HomeView(ProductFilterMixin, ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'


class ShopView(ProductFilterMixin, ListView):
    model = Product
    template_name = 'shop/shop.html'
    context_object_name = 'products'


class CategoryProductsView(ListView):
    model = Product
    template_name = 'shop/category_products.html'
    context_object_name = 'products'
    paginate_by = 6

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
    paginate_by = 6

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


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'პროდუქტი "{form.instance.name}" წარმატებით დაემატა.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Product'
        context['button_text'] = 'Create Product'
        context['categories'] = get_annotated_categories()
        return context

    def get_success_url(self):
        return reverse('shop:product_detail', kwargs={'product_id': self.object.id})


@login_required
def product_update_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'პროდუქტი "{product.name}" წარმატებით განახლდა.')
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


@login_required
def product_delete_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        product_title = product.name
        product.delete()
        messages.success(request, f'პროდუქტი "{product_title}" წარმატებით წაიშალა.')
        return redirect('shop:home')

    context = {
        'product': product,
        'categories': get_annotated_categories(),
    }
    return render(request, 'shop/product_confirm_delete.html', context)