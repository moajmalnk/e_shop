from django.shortcuts import render, redirect, get_object_or_404
from e_shopee.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_pk):
    products = Product.objects.get(id=product_pk)
    try:
        cart = Cart.objects.get(cart_id=request.user.id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=products, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=products,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('cart:cart_details')


def cart_details(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=request.user.id)
        cart_items = CartItem.objects.filter(cart=cart, active=True)[0]
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))


def cart_remove(request, product_pk):
    cart = Cart.objects.get(cart_id=request.user.id)
    product = get_object_or_404(Product, id=product_pk)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_details')


def full_remove(request, product_pk):
    cart = Cart.objects.get(cart_id=request.user.id)
    product = get_object_or_404(Product, id=product_pk)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_details')
