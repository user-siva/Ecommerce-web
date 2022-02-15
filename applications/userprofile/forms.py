from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.layout import Submit,Button
from crispy_forms.helper import FormHelper
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = '__all__'
		exclude = ('user',)

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=50,required=True,widget=forms.TextInput(attrs={'class' : 'entry'}))
	last_name = forms.CharField(max_length=50,required=True,widget=forms.TextInput(attrs={'class' : 'entry'}))
	email = forms.EmailField(max_length=50,required=True,widget=forms.TextInput(attrs={'class' : 'entry'}))
	class Meta:
		model = User
		fields = ['first_name','last_name','username','email','password1','password2']