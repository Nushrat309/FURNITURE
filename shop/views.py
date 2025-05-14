from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product, Cart, CartItem,Order,OrderItem

from django.http import HttpResponse, JsonResponse
# Create your views here.

def shop(request):
    data = Product.objects.all()
    return render(request, 'shop.html', {'data': data})



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    next_url = request.GET.get('next', 'shop')  # Default to 'shop' if no next URL is provided

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Respond with JSON for AJAX requests
            return JsonResponse({
                'success': True,
                'message': 'Product added to cart.',
                'cart_count': cart.items.count()
            })
        else:
            return redirect(next_url)  # Redirect to the referring page
    else:
        # Handle session-based cart for non-authenticated users
        cart = request.session.get('cart', {})
        if str(product_id) not in cart:
            cart[str(product_id)] = {'quantity': 1, 'price': str(product.price)}
        else:
            cart[str(product_id)]['quantity'] += 1
        request.session['cart'] = cart  # Update the session

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Respond with JSON for AJAX requests
            return JsonResponse({
                'success': True,
                'message': 'Product added to cart.',
                'cart_count': len(request.session['cart'])
            })
        else:
            return redirect(next_url)  # Redirect to the referring page


def view_cart(request):
    if request.user.is_authenticated:
        # Handle authenticated users
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()
        # Add total_price to each item in the cart
        items_with_total = [
            {
                'product': item.product,
                'quantity': item.quantity,
                'total_price': float(item.product.price) * item.quantity  # Calculate total price for each CartItem
            }
            for item in items
        ]
        # Calculate subtotal using CartItem objects
        subtotal = sum(item['total_price'] for item in items_with_total)
    else:
        # Handle anonymous users with session-based cart
        cart = request.session.get('cart', {})
        items_with_total = [
            {
                'product': get_object_or_404(Product, id=prod_id),
                'quantity': details['quantity'],
                'price': details['price'],
                'total_price': float(details['price']) * details['quantity'],  # Calculate total price for each item
            }
            for prod_id, details in cart.items()
        ]
        # Calculate subtotal for session-based cart
        subtotal = sum(item['total_price'] for item in items_with_total)
    
    # Define shipping cost
    shipping_cost = 50
    # Calculate total
    total = subtotal + shipping_cost

    context = {
        'items': items_with_total,  # Pass the modified list with total_price
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total,
    }
    
    return render(request, 'cart.html', context)



def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        # Handle authenticated users
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=item_id)
        cart_item.delete()
    else:
        # Handle non-authenticated users (session-based cart)
        cart = request.session.get('cart', {})
        if str(item_id) in cart:
            del cart[str(item_id)]
            request.session['cart'] = cart  # Update the session
    
    return redirect('cart')

def update_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # For authenticated users
            cart, created = Cart.objects.get_or_create(user=request.user)
            for item_id, quantity in request.POST.items():
                if item_id.startswith('quantity_'):
                    try:
                        product_id = item_id.split('_')[1]
                        quantity = int(quantity)
                        product = get_object_or_404(Product, id=product_id)

                        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
                        if cart_item:
                            if quantity <= 0:
                                cart_item.delete()
                            else:
                                cart_item.quantity = quantity
                                cart_item.save()
                    except (ValueError, IndexError):
                        continue  # Skip bad inputs
        else:
            # For non-authenticated users (session-based cart)
            session_cart = request.session.get('cart', {})
            for item_id, quantity in request.POST.items():
                if item_id.startswith('quantity_'):
                    try:
                        product_id = item_id.split('_')[1]
                        quantity = int(quantity)

                        if product_id in session_cart:
                            if quantity <= 0:
                                del session_cart[product_id]
                            else:
                                session_cart[product_id]['quantity'] = quantity
                    except (ValueError, IndexError):
                        continue
            request.session['cart'] = session_cart

        return redirect('cart')  # Ensure 'cart' is a valid URL name
    else:
        return HttpResponse(status=405)



def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    subtotal = sum(float(item.product.price) * item.quantity for item in items)

    shipping_cost = 45
    total = subtotal + shipping_cost

    context = {
        'items': items,
        'subtotal' : subtotal,
        'shipping_cost' : shipping_cost,
        'total' : total
    }
    return render(request, 'checkout.html', context)


from django.contrib.auth.decorators import login_required
@login_required
def place_order(request):
    if request.method == "POST":
        user = request.user  # This is a User instance

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return redirect('cart')

        billing_address = request.POST.get('billing_address')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        note = request.POST.get('note')

        cart_items = CartItem.objects.filter(cart=cart)

        # Calculate total price
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Now create the order, including total_price
        order = Order.objects.create(
            user=user,
            billing_address=billing_address,
            name=name,
            email=email,
            phone=phone,
            note=note,
            total_price=total_price,
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity,
            )

        # Clean up cart (after the loop!)
        cart_items.delete()
        cart.delete()

        return redirect('home')

    return redirect('checkout')  # if not POST


