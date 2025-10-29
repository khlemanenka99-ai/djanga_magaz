from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True)

class ProductImage(models.Model):
    objects = models.Manager()

    detail_images = models.ImageField(upload_to='images/', blank=True, null=True)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.SET_NULL, null=True, blank=True)

# class Orders(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     status = models.CharField(max_length=50, default='Новый')
#     address = models.CharField(max_length=255, help_text='Адрес доставки')
#     phone = models.CharField(max_length=20, help_text='Телефон клиента')
#
# class OrderItem(models.Model):
#     orders = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='items')
#     product_name = models.CharField(max_length=255)
#     product_price = models.DecimalField(max_digits=10, decimal_places=2)

