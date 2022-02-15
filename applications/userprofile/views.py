from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm,UserProfileForm

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		userProfileForm = UserProfileForm(request.POST)

		if form.is_valid() and userProfileForm.is_valid():
			user = form.save()
			userprofile = userProfileForm.save(commit=False)
			userprofile.user = user
			userprofile.save()

			login(request,user)

			return redirect('frontpage')
	else:
		form = SignUpForm()
		userProfileForm = UserProfileForm(request.POST)

	return render(request,'signup.html',{'form':form,'user_profile_form':userProfileForm})

@login_required
def myAccount(request):
	return render(request,'myAccount.html')