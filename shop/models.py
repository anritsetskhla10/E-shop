from django.db import models

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="კატეგორიის სახელი")
    description = models.TextField(blank=True, null=True, verbose_name="აღწერა")

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="კატეგორია"
    )
    name = models.CharField(max_length=200, verbose_name="პროდუქტის სახელი")
    description = models.TextField(verbose_name="აღწერა")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ფასი")
    is_on_sale = models.BooleanField(default=False, verbose_name="ფასდაკლება")
    is_available = models.BooleanField(default=True, verbose_name="ხელმისაწვდომობა")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
