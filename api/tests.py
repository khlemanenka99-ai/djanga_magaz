from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from myapp.models import Product


class RegistrationFormTests(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.create_order = reverse('create_order')


    def test_registration_valid_data(self):
        data = {
            'username': 'newuser',
            'password': 'ComplexPassword123',
            'password2': 'ComplexPassword123',
            'email': 'newuser@example.com',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_registration_password_mismatch(self):
        data = {
            'username': 'user2',
            'password': 'Password1',
            'password2': 'Password2',  # не совпадают
            'email': 'user2@example.com',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Пароли не совпадают")

    def test_order_valid_data(self):
        data = {
            'address': 'Minsk',
            'phone': '1234567'
        }
        response = self.client.post(self.create_order, data)
        self.assertEqual(response.status_code, 302)

class CartTest(TestCase):
    def setUp(self):
        # Создаем юзера
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        # Создаем тестовый продукт
        self.product = Product.objects.create(name='Test Product', price='1', in_stock=True, quantity=10)

    def test_add_in_stock_product(self):
        url = reverse('add_to_cart', kwargs={'product_id': self.product.pk})
        response = self.client.post(url, {'quantity': 1})
        self.assertRedirects(response, reverse('cart_view'))

        # Проверяем, что товар добавился в корзину
        session = self.client.session
        cart = session.get('cart', {})
        self.assertEqual(cart.get(str(self.product.pk)), 1)

    def test_add_not_in_stock_product(self):
        # Создаем товар, которого нет в наличии
        not_in_stock_product = Product.objects.create(
            name='Out of stock',
            price='1',
            in_stock=False,
            quantity=0
        )
        url = reverse('add_to_cart', kwargs={'product_id': not_in_stock_product.pk})
        response = self.client.post(url)
        self.assertTemplateUsed(response, 'in_stock.html')


