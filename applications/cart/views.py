from django.shortcuts import render
from django.conf import settings
from .cart import Cart
import json

def cart_detail(request):
	cart = Cart(request)
	productstring = ''
	for item in cart:
		product = item['product']
		b = "{'id': '%s', 'title': '%s', 'price': '%s', 'quantity': '%s','total_price':'%s','num_available':'%s'}," % (product.id, product.title, product.price, item['quantity'],item['total_price'],product.num_available) 
		productstring = productstring + b

	if request.user.is_authenticated:
		first_name = request.user.first_name
		last_name = request.user.last_name
		email = request.user.email
	else:
		first_name = last_name = email = ''

	message='secret'
	context = {
		'first_name':first_name,
		'last_name':last_name,
		'email':email,
		'cart':cart,
		'productstring':productstring,
		'message':message,
		'public_key':settings.STRIPE_API_KEY_PUBLISHABLE
	}

	return render(request,'cart.html',context)

def success(request):
	cart = Cart(request)
	cart.clear()
	return render(request,'success.html')