from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Product, Cart, CartItem
from django.contrib.auth.models import User
from .forms import MobileLoginForm
from .models import Product, Order  # Order model ko create karna hoga
from django.contrib import messages
from datetime import timedelta, date


# ✅ HOME VIEW
def home_view(request):
    return render(request, 'myapp/home.html')  # No menu items here

# ✅ ABOUT PAGE
def about_view(request):
    return render(request, 'myapp/about.html')

# ✅ MENU VIEW (show all products here)
def menu_view(request):
    products = Product.objects.all()
    return render(request, 'myapp/menu.html', {'products': products})

# ✅ CART VIEWS
@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
    items = cart.cart_items.select_related('product').all()
    
    total = 0
    for item in items:
        item.total_price = item.product.price * item.quantity
        total += item.total_price

    delivery_charge = 40
    grand_total = total + delivery_charge

    expected_delivery = date.today() + timedelta(days=3)

    return render(request, 'myapp/cart.html', {
        'cart': cart,
        'items': items,
        'total': total,
        'delivery_charge': delivery_charge,
        'grand_total': grand_total,
        'expected_delivery': expected_delivery.strftime('%A, %d %B'),
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')

@login_required
def delete_cart_item(request, item_id):
    get_object_or_404(CartItem, id=item_id, cart__user=request.user).delete()
    return redirect('view_cart')

# ✅ ORDER PAGE
def order_view(request, product_id):
    from .models import Product
    from django.shortcuts import get_object_or_404

    product = get_object_or_404(Product, id=product_id)
    return render(request, 'myapp/order.html', {'product': product})



def place_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        total_price = product.price * quantity

        new_order = Order.objects.create(
            customer_name=name,
            phone=phone,
            address=address,
            quantity=quantity,
            product=product,
            total_price=total_price
        )

        # After placing order, redirect or show success page
        return render(request, 'myapp/order_success.html', {
            'name': name,
            'product': product,
            'total_price': total_price,
            'order': new_order
        })

    else:
        # Show the form again if GET request
        products = Product.objects.all()
        return render(request, 'myapp/place_order.html', {'products': products})

@login_required
def checkout_view(request):
    return render(request, 'myapp/checkout.html')

def login_view(request):
    next_url = request.GET.get('next', 'home')  # ✅ fetch next value from URL

    if request.method == 'POST':
        form = MobileLoginForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data['mobile']
            password = form.cleaned_data['password']
            name = form.cleaned_data.get('name', '')

            user = authenticate(request, username=mobile, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)  # ✅ after login
            else:
                try:
                    user = User.objects.create_user(username=mobile, password=password, first_name=name)
                    login(request, user)
                    return redirect(next_url)  # ✅ after signup
                except Exception as e:
                    form.add_error(None, f"Error creating account: {str(e)}")
    else:
        form = MobileLoginForm()

    return render(request, 'myapp/login.html', {'form': form})

# ✅ BOOK TABLE
def book_table_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        occasion = request.POST.get('occasion')
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests = request.POST.get('guests')
        table_pref = request.POST.get('table_preference')
        message_text = request.POST.get('message')
        payment_method = request.POST.get('payment_method')

        booking = TableBooking.objects.create(
            name=name,
            phone=phone,
            email=email,
            occasion=occasion,
            date=date,
            time=time,
            guests=guests,
            table_preference=table_pref,
            message=message_text,
            payment_method=payment_method,
            is_paid=True
        )

        messages.success(request, '🎉 Booking Confirmed! Thank you for booking with us.')
        return redirect('book_table_view')

    return render(request, 'myapp/book_table.html')
# ✅ LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')

