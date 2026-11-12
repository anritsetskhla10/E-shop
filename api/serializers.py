from rest_framework import serializers
from shop.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    author = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'image',
            'is_on_sale',
            'is_available',
            'category',
            'category_name',
            'author',
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    author = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'image',
            'is_available',
            'is_on_sale',
            'category',
            'author',
        ]


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'image',
            'category',
            'is_available',
            'is_on_sale',
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('პროდუქტის ფასი უნდა იყოს 0-ზე მეტი.')
        return value