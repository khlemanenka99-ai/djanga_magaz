from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegisterForm
from .models import Product, Category


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # хэшируем пароль
            user.save()
            login(request, user)  # сразу авторизуем пользователя
            return redirect('products')  # редирект на список товаров
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



def products_view(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    products = Product.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)
    return render(request, 'products.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
    })

@login_required(login_url='/login/')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    product = get_object_or_404(Product, pk=product_id)
    if product.in_stock == True:
        cart.append(product_id)
        if product_id not in cart:
            cart[product_id] = cart.get(product_id, 0) + 1
    elif product.in_stock == False:
        return render(request,'in_stoc.html', {'product': product})
    request.session['cart'] = cart
    return redirect('cart_view')


@login_required(login_url='/login/')
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
    request.session['cart'] = cart
    return redirect('cart_view')

@login_required(login_url='/login/')
def cart_view(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    total = sum(p.price for p in products)
    return render(request, 'cart.html', {'products': products, 'total': total})

# @login_required(login_url='/login/')
# def create_order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             orders = form.save(commit=False)
#             orders.user = request.user
#             orders.save()
#             cart = request.session.get('cart', [])
#             products = Product.objects.filter(id__in=cart)
#
#             product_name = Product.name
#             product_price = Product.price
#
#
#             OrderItem.objects.create(
#                 orders=orders,
#                 product_name=product_name,
#                 product_price=product_price,
#             )
#
#             orders.save()
#             request.session['cart'] = {}
#
#             return redirect('success')
#     else:
#         form = OrderForm()
#
#     return render(request, 'create_order.html', {'form': form})


# TELEGRAM_BOT_TOKEN = '7800961465:AAGUnuhuN7EBnYbe1t6CmOOPvnZtOUC3-Jo'
# TELEGRAM_CHAT_ID = 't.me/MatraCKS_bot.'  # либо ваш личный чат или чат магазина
#
# def send_telegram_message(message):
#     url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
#     data = {
#         'chat_id': TELEGRAM_CHAT_ID,
#         'text': message,
#     }
#     requests.post(url, data=data)

