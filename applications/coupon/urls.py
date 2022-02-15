from django.urls import path
from . import views,api

urlpatterns = [
	path('api/can_use/',api.api_can_use,name='api_can_use'),

]