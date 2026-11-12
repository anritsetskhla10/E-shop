from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view(), name='category_list'),
    path('products/', views.ProductListAPIView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product_detail'),
    path('products/create/', views.ProductCreateAPIView.as_view(), name='product_create'),
]