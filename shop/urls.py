from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Read & General Pages
    path('', views.home_view, name='home'),
    path('shop/', views.shop_view, name='shop'),
    path('category/<int:category_id>/', views.category_products_view, name='category_products'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('sale/', views.sale_products_view, name='sale_products'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('contact/', views.contact_view, name='contact'),

    # Product CRUD Operations
    path('product/create/', views.product_create_view, name='product_create'),
    path('product/<int:product_id>/update/', views.product_update_view, name='product_update'),
    path('product/<int:product_id>/delete/', views.product_delete_view, name='product_delete'),
]