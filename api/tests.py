
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse

from myapp.models import Product
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from datetime import timedelta

from myapp.models import Orders


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
        session = self.client.session
        session['cart'] = {
            '10': 1
        }
        session.save()
        data = {
            'address': 'Minsk',
            'phone': '1234567'
        }
        response = self.client.post(reverse('create_order'), data)
        self.assertEqual(response.status_code, 302)
        redirect_url = response['Location']
        self.assertIn('create_order', redirect_url)
        # Проверка, что заказ появился в базе
        print("Все заказы:", list(Orders.objects.all()))

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
#
class SimpleJWTTest(APITestCase):
    def setUp(self):
        # Создаём обычного пользователя
        self.user = User.objects.create_user(username='user1', password='pass123')

    def test_can_access_protected_api(self):
        # Генерируем JWT токен для пользователя
        token = str(AccessToken.for_user(self.user))

        # Делаем GET-запрос к защищённому эндпоинту с токеном
        response = self.client.get(
            '/api/products/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        # Проверяем, что сервер не вернул 401 Unauthorized
        self.assertNotEqual(response.status_code, 401)

    def test_not_access_protected_api(self):
        # Делаем GET-запрос к защищённому эндпоинту без токена
        response = self.client.get(
            '/api/products/'
        )
        # Проверяем, что сервер вернул 401 Unauthorized
        self.assertEqual(response.status_code, 401)

    def test_access_with_expired_token(self):
        # Создайте токен, который уже истёк
        expired_token = AccessToken.for_user(self.user)
        # Установите время истечения в прошлое
        expired_token.set_exp(from_time=None, lifetime=timedelta(seconds=-1))
        token_str = str(expired_token)
        response = self.client.get(
            '/api/products/',
            HTTP_AUTHORIZATION=f'Bearer {token_str}'
        )
        # Проверка, что сервер возвращает 401 Unauthorized для просроченного токена
        self.assertEqual(response.status_code, 401)
