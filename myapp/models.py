from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal

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
    quantity = models.PositiveSmallIntegerField(blank=False, null=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    @property
    def price_sale(self):
        return self.price * Decimal('0.75')

    # @property
    # def price_with_vat(self):
    #     return self.price * Decimal('1.2')

    def save(self, *args, **kwargs):
        self.in_stock = self.quantity > 0
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    objects = models.Manager()

    detail_images = models.ImageField(upload_to='images/', blank=True, null=True)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.SET_NULL, null=True, blank=True)

class Orders(models.Model):
    objects = models.Manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('paid', 'Оплачен'),
        ('sent', 'Отправлен'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    address = models.CharField(max_length=255, help_text='Адрес доставки')
    phone = models.CharField(max_length=20, help_text='Телефон клиента')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=False,
    )
    quantity = models.PositiveSmallIntegerField(default=1)



