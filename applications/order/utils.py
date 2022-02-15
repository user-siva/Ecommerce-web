import datetime,os
from applications.cart.cart import Cart
from .models import Order,OrderItem
from random import randint

def checkout(request,first_name,last_name,email,address,zipcode,place):
	order = Order(first_name=first_name,last_name=last_name,email=email,address=address,zipcode=zipcode,place=place)
	if request.user.is_authenticated:
		order.user = request.user
	order.save()

	cart = Cart(request)

	for item in cart:
		orderItem = OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])

	return order.id