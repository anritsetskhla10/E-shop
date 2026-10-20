from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Read & General Pages
    path('', views.HomeView.as_view(), name='home'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('category/<int:category_id>/', views.CategoryProductsView.as_view(), name='category_products'),
    path('product/<int:product_id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('sale/', views.SaleProductsView.as_view(), name='sale_products'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('contact/', views.ContactView.as_view(), name='contact'),

    # Product CRUD Operations
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<int:product_id>/update/', views.product_update_view, name='product_update'),
    path('product/<int:product_id>/delete/', views.product_delete_view, name='product_delete'),
]