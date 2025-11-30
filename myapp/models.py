from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
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
    discount_percent = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    @property
    def discounted_price(self):
        discount_multiplier = Decimal('1') - Decimal(self.discount_percent) / Decimal('100')
        return self.price * discount_multiplier

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


class Cart(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    price_at_addition = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Цена продукта на момент добавления в корзину'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text='Количество товара'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )

    def __str__(self):
        return f"{self.product.name} x {self.quantity} (Пользователь: {self.user.username})"

    @property
    def total_price(self):
        """Общая стоимость этого элемента корзины"""
        return self.price_at_addition * self.quantity

    def save(self, *args, **kwargs):
        # фиксируем текущую цену продукта
        if not self.pk:
            self.price_at_addition = self.product.price
        super().save(*args, **kwargs)

