from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import *
from .forms import *

# FUNCTIONS #
def GET_USER_ITEMS(user):
	if user.is_authenticated:
		return Item.objects.filter(user=user)

# VIEWS #
def index(request):
	context = {
		'indexPage': True,
		'items': GET_USER_ITEMS(request.user)
	}
	
	return render(request, "index.html", context)

@login_required
def account(request):
	context = {
		'username': request.user,
		'items': GET_USER_ITEMS(request.user)
	}

	return render(request, "account/account.html", context)

@login_required
def add_item(request):
	if request.method == "POST" and request.user.is_authenticated:
		newItemForm = NewItemForm(request.POST)

		if newItemForm.is_valid():
			Item(
				user = request.user,
				name = newItemForm.cleaned_data.get("name"),
				cost = newItemForm.cleaned_data.get("cost"),
				price = newItemForm.cleaned_data.get("price"),
				details = newItemForm.cleaned_data.get("details")
			).save()

			return HttpResponseRedirect("/account/")
	else:
		newItemForm = NewItemForm()
	
	context = {
		'form': newItemForm
	}

	return render(request, "account/add_item.html", context)

@login_required
def add_item_images(request, itemID):
	item = Item.objects.get(id=itemID)
	
	if request.user == item.user:
		if request.method == "POST":
			newImageForm = NewImageForm(request.POST, request.FILES)

			if newImageForm.is_valid():
				ItemImage(
					item = item,
					img = newImageForm.cleaned_data.get("img"),
					desc = newImageForm.cleaned_data.get("desc")
				).save()
				
				return HttpResponseRedirect("/account/")
		else:
			newImageForm = NewImageForm()
	else:
		return HttpResponseRedirect("/account/")
	
	context = {
		'form': newImageForm,
		'item': item
	}

	return render(request, "account/add_item_images.html", context)

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
			return HttpResponseRedirect("/account/")
	else:
		regForm = RegistrationForm()
	
	context = {
		'form': regForm
	}
	
	return render(request, "registration/register.html", context)