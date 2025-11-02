from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegisterForm, OrderForm
from .models import Product, Category, OrderItem


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('products')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



def products_view(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    products = Product.objects.all()
    query = request.GET.get('q')
    if category_id:
        products = products.filter(category_id=category_id)
    if query:
        products = products.filter(
            Q(name__icontains=query)
        )
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
def add_to_cart(request, product_id, quantity=1):
    cart = request.session.get('cart', {})

    product = get_object_or_404(Product, pk=product_id)
    if not product.in_stock:
        return render(request, 'in_stock.html', {
            'product': product,
        })
    if product.quantity < quantity:
        return render(request, 'in_stock.html', {
            'product': product,
        })

    product_id_str = str(product_id)
    if product_id_str in cart:
        new_quantity = cart[product_id_str] + quantity
        if new_quantity > product.quantity:
            new_quantity = product.quantity
        cart[product_id_str] = new_quantity
    else:
        if quantity > product.quantity:
            quantity = product.quantity
        cart[product_id_str] = quantity

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_view')


@login_required(login_url='/login/')
def remove_from_cart(request, product_id, quantity=1):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, pk=product_id)

    product_id_str = str(product_id)

    if product_id_str in cart:
        current_quantity = cart[product_id_str]
        if current_quantity > quantity:
            cart[product_id_str] = current_quantity - quantity
        else:
            del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
    else:
        return render(request, 'cart.html', {
            'message': 'Товар отсутствует в корзине.',
            'cart': cart
        })

    return redirect('cart_view')

@login_required(login_url='/login/')
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id_str, quantity in cart.items():
        product = get_object_or_404(Product, pk=int(product_id_str))
        total = product.price * quantity
        total_price += total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total
        })
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required(login_url='/login/')
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            cart = request.session.get('cart', {})
            if not cart:
                return render(request, 'create_order.html', {
                    'form': form,
                    'error_message': 'Ваша корзина пуста.'
                })

            for product_id_str, quantity in cart.items():
                product_id = int(product_id_str)
                product = get_object_or_404(Product, pk=product_id)

                if not product.in_stock or product.quantity < quantity:
                    return render(request, 'create_order.html', {
                        'form': form,
                        'error_message': '.'
                    })

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )

            request.session['cart'] = {}
            request.session.modified = True

            return render(request, 'success.html')
    else:
        form = OrderForm()

    return render(request, 'create_order.html', {'form': form})


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

