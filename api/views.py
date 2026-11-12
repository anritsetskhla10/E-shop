from rest_framework import generics, permissions
from shop.models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductCreateSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)


class CategoryListAPIView(generics.ListAPIView):
    """GET /api/categories/ - კატეგორიების სია."""
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductListAPIView(generics.ListAPIView):
    """GET /api/products/ - ხელმისაწვდომი პროდუქტების სია."""
    queryset = Product.objects.filter(is_available=True).order_by('-id')
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]


class ProductDetailAPIView(generics.RetrieveAPIView):
    """GET /api/products/<int:pk>/ - პროდუქტის დეტალური ინფორმაცია."""
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]


class ProductCreateAPIView(generics.CreateAPIView):
    """POST /api/products/create/ - ახალი პროდუქტის შექმნა."""
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)