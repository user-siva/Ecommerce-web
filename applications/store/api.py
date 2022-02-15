from django.shortcuts import render,get_object_or_404,redirect
from applications.cart.cart import Cart
from .models import *
from django.http import JsonResponse
import json
from applications.order.utils import checkout
from applications.order.models import Order,OrderItem
import stripe
from django.conf import settings
from applications.coupon.models import Coupon

def create_checkout_session(request):
	cart = Cart(request)
	stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
	data = json.loads(request.body)

	coupon_code = data['coupon_code']
	coupon_value = 0

	if coupon_code!='':
		coupon = Coupon.objects.get(code=coupon_code)
		if coupon.can_use():
			coupon_value = coupon.value
			coupon.use()

	items = []

	for item in cart:
		product = item['product']

		price=int(product.price*100)
		if coupon_value>0:
			price = int(price * (int(coupon_value)/100))
			print('price:',price)

		obj = {
			'price_data':{
				'currency':'inr',
				'product_data':{
					'name':product.title
				},
				'unit_amount':price,
			},
			'quantity':item['quantity'],

		}	

	items.append(obj)

	session = stripe.checkout.Session.create(
		payment_method_types = ['card',],
		line_items = items,
		mode = 'payment',
		success_url = 'http://127.0.0.1:8000/cart/success',
		cancel_url = 'http://127.0.0.1:8000/cart/',

	)

	jsonresponse = {'SUCCESS':True}

	first_name = data['first_name']
	last_name = data['last_name']
	email = data['email']
	address = data['address']
	zipcode = data['zipcode']
	place = data['place']
	payment_intent = session.payment_intent

	orderid = checkout(request,first_name,last_name,email,address,zipcode,place)

	total_price = 0.00

	if coupon_value>0:
		total_price = total_price * (coupon_value/100)

	order = Order.objects.get(pk=orderid)
	order.payment_intent = payment_intent
	order.paid_amount = cart.get_total_cost()
	order.used_coupon = coupon_code

	order.save()

	return JsonResponse({'session':session})

def api_add_to_cart(request):
	data = json.loads(request.body)
	jsonresponse = {'SUCCESS':True}
	product_id = data['product_id']
	update = data['update']
	quantity = data['quantity']

	product = get_object_or_404(Product,pk=product_id)
	print('title',product.title)
	cart = Cart(request)

	if not update:
		cart.add(product=product,quantity=1,update_quantity=False)
	else:
		cart.add(product=product,quantity=quantity,update_quantity=True)

	return JsonResponse(jsonresponse)

def api_remove_from_cart(request):
	
	data = json.loads(request.body)
	jsonresponse = {'SUCCESS':True}
	product_id = str(data['product_id'])

	cart = Cart(request)

	cart.remove(product_id)

	return JsonResponse(jsonresponse)

def api_checkout(request):
	data = json.loads(request.body)
	jsonresponse = {'SUCCESS':True}

	first_name = data['first_name']
	last_name = data['last_name']
	email = data['email']
	address = data['address']
	zipcode = data['zipcode']
	place = data['place']

	orderid = checkout(request,first_name,last_name,email,address,zipcode,place)
	cart = Cart(request)

	paid = True

	if paid == True:
		order = Order.objects.get(pk=orderid)
		order.paid_amount = cart.get_total_cost()
		order.paid = True
		order.save()

		cart.clear()

	return JsonResponse(jsonresponse)

































