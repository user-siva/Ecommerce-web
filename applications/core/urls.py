from django.urls import path
from . import views

urlpatterns = [
	path('',views.frontpage,name='frontpage'),
	path('contact/',views.contact,name='contact'),
	path('about/',views.about,name='about'),
	path('order_confirmation/',views.order_confirmation,name='order_confirmation'),
	
]