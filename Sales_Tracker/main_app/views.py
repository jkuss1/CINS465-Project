from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import *
from .forms import *

# FUNCTIONS #
def GET_USER_ITEMS(user):
	if user.is_authenticated:
		items = Item.objects.filter(user=user)

		for item in items:
			item.image_set = ItemImage.objects.filter(item=item)
		
		return items

# VIEWS #
def index(request):
	context = {
		'index_page': True,
		'user_items': GET_USER_ITEMS(request.user)
	}
	
	return render(request, "index.html", context)

@login_required
def account(request):
	context = {
		'username': request.user,
		'user_items': GET_USER_ITEMS(request.user)
	}

	return render(request, "account/account.html", context)

@login_required
def add_item(request):
	if request.method == "POST" and request.user.is_authenticated:
		new_item_form = NewItemForm(request.POST)

		if new_item_form.is_valid():
			Item(
				user = request.user,
				name = new_item_form.cleaned_data.get("name"),
				cost = new_item_form.cleaned_data.get("cost"),
				price = new_item_form.cleaned_data.get("price"),
				details = new_item_form.cleaned_data.get("details")
			).save()

			return HttpResponseRedirect("/account/")
	else:
		new_item_form = NewItemForm()
	
	context = {
		'form': new_item_form
	}

	return render(request, "account/add_item.html", context)

@login_required
def add_item_images(request, itemID):
	item = Item.objects.get(id=itemID)
	
	if request.user == item.user:
		if request.method == "POST":
			new_image_form = NewImageForm(request.POST, request.FILES)

			if new_image_form.is_valid():
				ItemImage(
					item = item,
					file = new_image_form.cleaned_data.get("file"),
					alt = new_image_form.cleaned_data.get("alt")
				).save()
				
				return HttpResponseRedirect("/account/")
		else:
			new_image_form = NewImageForm()
	else:
		return HttpResponseRedirect("/account/")
	
	context = {
		'form': new_image_form,
		'item': item
	}

	return render(request, "account/add_item_images.html", context)

def register(request):
	if request.method == "POST":
		reg_form = RegistrationForm(request.POST)

		if reg_form.is_valid():
			user = reg_form.save()
			user = authenticate(
				username = reg_form.cleaned_data.get("username"),
				password = reg_form.cleaned_data.get("password1")
			)

			login(request, user)
			return HttpResponseRedirect("/account/")
	else:
		reg_form = RegistrationForm()
	
	context = {
		'form': reg_form
	}
	
	return render(request, "registration/register.html", context)