from .cart import Cart
from django.core.handlers.wsgi import WSGIRequest

def cart(request: WSGIRequest):
    return {'cart': Cart(request)}