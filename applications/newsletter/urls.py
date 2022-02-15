from django.urls import path
from . import views,api

urlpatterns = [
	path('api/add_subscriber/',api.api_add_subscriber,name='api_add_subscriber'),

]