from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import *
from .forms import *

# Create your views here.
def index(request):
	context = {
		'indexPage': True
	}
	
	return render(request, "index.html", context)

@login_required
def account(request):
	context = {
		'username': request.user
	}

	return render(request, "account/account.html", context)

def register(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)

		if form.is_valid():
			user = form.save()
			user = authenticate(
				username = form.cleaned_data.get("username"),
				password = form.cleaned_data.get("password1")
			)

			login(request, user)
			return HttpResponseRedirect('/account/')
	else:
		form = RegistrationForm()
	
	context = {
		'form': form
	}
	
	return render(request, "registration/register.html", context)