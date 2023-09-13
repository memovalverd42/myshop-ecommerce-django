from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.handlers.wsgi import WSGIRequest
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender
from typing import List

def cart_detail(request: WSGIRequest) -> render:
    ''' Vista para mostrar detalles del carrito '''
    cart = Cart(request)
    
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                            initial={
                                                'quantity': item['quantity'],
                                                'override': True
                                            }
                                        )
    coupon_apply_form = CouponApplyForm()
    
    r = Recommender()
    cart_products: List[Product] = [item['product'] for item in cart]
    if(cart_products):
        recommended_products = r.suggest_products_for(
                                cart_products,
                                max_results=4)
    else:
        recommended_products = []
    
    
    return render(
        request,
        'cart/detail.html',
        { 
         'cart': cart,
         'coupon_apply_form': coupon_apply_form,
         'recommended_products': recommended_products
        }
    )

@require_POST
def cart_add(request: WSGIRequest, product_id: int) -> redirect:
    ''' Vista para menejar el añadir un producto al carrito '''
    cart = Cart(request)
    product: Product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product, quantity=cd['quantity'], override_quantity=cd['override'])
        
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request: WSGIRequest, product_id: int) -> redirect:
    ''' Vista para menejar el remover un producto del carrito '''
    cart: Cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

