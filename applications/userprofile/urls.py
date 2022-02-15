from django.urls import path
from . import views

urlpatterns = [
	path('signup/',views.signup,name='signup'),
	path('myaccount/',views.myAccount,name='myaccount'),
]