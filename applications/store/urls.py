from django.urls import path
from . import views,api

urlpatterns = [
	path('<int:pk>/',views.ProductDetail,name='product_detail'),
	path('category/<int:pk>/',views.CategoryDetail,name='category_detail'),
	path('search/',views.search,name='search'),


	path('api/add_to_cart/',api.api_add_to_cart,name='api_add_to_cart'),
	path('api/remove_from_cart/',api.api_remove_from_cart,name='api_remove_from_cart'),
	path('api/create_checkout_session/',api.create_checkout_session,name='create_checkout_session'),

]