from django.shortcuts import render,get_object_or_404
from applications.store.models import *
from applications.cart.cart import Cart
from applications.order.models import Order

def frontpage(request):
	cart = Cart(request)
	products = Product.objects.filter(is_featured=True)
	product = Product.objects.all()
	product_name = cart.product_name()
	print('product_name',product_name)
	context = {
		'cart':cart,
		'products':products,
		'product':product,
	}
	return render(request,'frontpage.html',context)

def order_confirmation(request):
	order = Order.objects.get(pk=32)
	return render(request,'order_confirmation.html',{'order':order})

def contact(request):
	context = {

	}
	return render(request,'contact.html',context)

def about(request):
	context = {

	}
	return render(request,'about.html',context)