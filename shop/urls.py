from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('category/<int:category_id>/', views.category_products_view, name='category_products'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('sale/', views.sale_products_view, name='sale_products'),
]