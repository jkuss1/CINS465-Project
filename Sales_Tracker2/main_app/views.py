from django.shortcuts import render, redirect
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from .models import *
from .forms import *

# Create your views here.
def index(request):
	context = {
		'indexPage': True
	}
	
	return render(request, "index.html", context)

class CalcPage(TemplateView):
	template_name = 'calc/calc.html'
	
class InputPage(TemplateView):
	template_name = 'input/input.html'
	
class SalesPage(TemplateView):
	template_name = 'sales/sales.html'
	
class InfoPage(TemplateView):
	template_name = 'info/info.html'	

@login_required
def account(request):
	context = {
		'username': request.user
	}

	return render(request, "account/account.html", context)

@login_required
def add_item(request):
	if request.method == "POST":
		newItemForm = NewItemForm(request.POST, request.FILES)

		if newItemForm.is_valid():
			item = newItemForm.save(user=request.user)
			item = authenticate(
				name = newItemForm.cleaned_data.get("name"),
				details = newItemForm.cleaned_data.get("details"),
				img = newItemForm.cleaned_data.get("img"),
				imgDesc = newItemForm.cleaned_data.get("imgDesc")
			)

			return HttpResponseRedirect('/account/')
	else:
		newItemForm = NewItemForm()
	
	context = {
		'form': newItemForm
	}

	return render(request, "account/add_item.html", context)

def register(request):
	if request.method == "POST":
		regForm = RegistrationForm(request.POST)

		if regForm.is_valid():
			user = regForm.save()
			user = authenticate(
				username = regForm.cleaned_data.get("username"),
				password = regForm.cleaned_data.get("password1")
			)

			login(request, user)
			return HttpResponseRedirect('/account/')
	else:
		regForm = RegistrationForm()
	
	context = {
		'form': regForm
	}
	
	return render(request, "registration/register.html", context)