from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.views.generic.detail import DetailView
from applications.cart.cart import Cart
from django.db.models import Q
import random

def search(request):
	query = request.GET.get("query")
	print('query',query)
	products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

	context = {
		'query':query,
		'products':products
	}

	return render(request,'search.html',context)

def ProductDetail(request,pk):
	product = get_object_or_404(Product, pk=pk)
	cart = Cart(request)

	if request.method == 'POST' and request.user.is_authenticated:
		stars = request.POST.get('stars',3)
		content = request.POST.get('content')

		review = ProductReview.objects.create(product=product,user=request.user,stars=stars,content=content)

		return redirect('product_detail', pk=pk)
	star_range = 0
	for i in product.reviews.all():
		star_range=i.stars
	print('star_range',star_range)

	related_products = list(product.category.products.filter(variant=None).exclude(id=product.id))
	if len(related_products)>=3:
		related_products = random.sample(related_products,3)

	if product.variant:
		return redirect('product_detail',pk=product.variant.pk)

	imagesString = "{'thumbnail':'%s','image':'%s'}," % (product.thumbnail.url,product.image.url)
	for image in product.images.all():
		imagesString = imagesString + ("{'thumbnail':'%s','image':'%s'}," % (image.thumbnail.url,image.image.url))

	cart = Cart(request)
	if cart.has_product(product.id):
		product.in_cart = True
	else:
		product.in_cart = False

	context = {
		'cart':cart,
		'product':product,
		'imagesString':imagesString,
		'related_products':related_products,
		'star_range':star_range,
	}
	return render(request,'product_detail.html',context)

def CategoryDetail(request,pk):
	category = get_object_or_404(Category,pk=pk)
	products = category.products.filter(variant=None)
	product = Product.objects.all()

	context = {
		'category':category,
		'products':products,
	}
	return render(request,'category_detail.html',context)

