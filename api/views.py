from pprint import pprint

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsManager, IsClient
from myapp.models import Product, Cart
from rest_framework.views import APIView

from api.serializers import ProductSerializer, RegisterSerializer, ProductDiscountSerializer, CartSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['GET'])
def test_api(request):

    products = Product.objects.all()
    category = request.query_params.get('category')
    if category:
        products = products.filter(category_id=category)
    data = [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price,
        } for product in products
    ]
    return Response(data)


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
        return Response({
            'id': product.id,
            'name': product.name,
            'price': product.price,
        })


class ProductListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Список продуктов",
        operation_description="Получение списка продуктов с фильтрацией",
        responses={
            200: ProductSerializer(many=True)
        },
    )

    @method_decorator(cache_page(60))
    def get(self, request):
        print('>>get')
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsManager]

    @swagger_auto_schema(
        operation_summary="Создание продукта",
        operation_description="Создает новый продукт",
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: 'Ошибки валидации'
        },
    )

    def post(self, request):
        serializer = ProductSerializer(data=request.data)  # десериализация входных данных
        if serializer.is_valid():  # проверка данных
            serializer.save()  # создание нового объекта Product
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        pprint(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def set_cookie_example(request):
    response = Response({'message': 'Cookie установлено'})
    response.set_cookie(
        key='user_token',
        value='12345abcdef',
        max_age=15,  # 15 сек
        httponly=True  # запрещает доступ к cookie из JS
    )
    return response


@api_view(['GET'])
def get_cookie_example(request):
    token = request.COOKIES.get('user_token')
    if token:
        return Response({'message': 'Cookie найден', 'token': token})
    return Response({'message': 'Cookie не найден'}, status=404)

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # регистрация открыта

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            # помечаем refresh в blacklist
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Token invalid or already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)

class SetDiscountAPIView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    @swagger_auto_schema(
        operation_summary="Создание скидки",
        operation_description="Делает скидку",
        request_body=ProductDiscountSerializer,
        responses={
            201: ProductDiscountSerializer,
            400: 'Ошибки валидации'
        },
    )

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductDiscountSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Discount updated",
                "product_id": product.id,
                "discount_percent": product.discount_percent
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    @swagger_auto_schema(
        operation_summary="Получение элементов корзины",
        operation_description="Просмотр товаров в корзине",
        responses={
            200: CartSerializer(many=True),
        }
    )
    def get(self, request):
        # Получение элементов корзины текущего пользователя
        queryset = Cart.objects.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Добавление товара в корзину",
        operation_description="Создаёт новый элемент в корзине",
        request_body=CartSerializer,
        responses={
            201: CartSerializer,
            400: 'Ошибки валидации'
        },
    )
    def post(self, request):
        # Создание нового элемента корзины
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            serializer.save(user=request.user, price_at_addition=product.price)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Удаление товара из корзины",
        operation_description="Удаляет товар",
        responses={
            204: 'Удалено успешно',
            400: 'Неверный ID или отсутствует',
            404: 'Элемент не найден'
        }
    )
    def delete(self, request, pk=None):
        # Удаление элемента корзины по ID
        if pk is None:
            return Response({'detail': 'ID элемента не предоставлено.'}, status=status.HTTP_400_BAD_REQUEST)
        cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

