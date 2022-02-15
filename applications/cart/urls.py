from django.urls import path
from . import views,webhook

urlpatterns = [
	path('cart/',views.cart_detail,name='cart_detail'),
	path('cart/success',views.success,name='success'),
	path('hooks/',webhook.webhook,name='webhook'),

]