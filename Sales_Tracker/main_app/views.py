import json
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import *
from .forms import *

# FUNCTIONS #
def GET_USER_ITEMS(user):
	items = None
	count = None
	
	if user.is_authenticated:
		items = Item.objects.filter(user=user)
		count = 0
		
		for item in items:
			count = count + 1
			item.images = []
			
			for image in ItemImage.objects.filter(item=item):
				item.images.append((image.file.url, image.alt))
	
	return items, count

def GET_ITEMS(start=0, end=25):
	items = Item.objects.all().order_by('-units_sold')[start:end]

	for item in items:
		item.images = []
		
		for image in ItemImage.objects.filter(item=item):
			item.images.append((image.file.url, image.alt))
	
	return items

# VIEWS #
def index(request):
	user_items, num_user_items = GET_USER_ITEMS(request.user)
	
	context = {
		'items': GET_ITEMS(0, 5),
		'user_items': user_items,
		'num_user_items': num_user_items
	}
	
	return render(request, 'index.html', context)

def all_items(request):
	context = {
		'items': GET_ITEMS()
	}
	
	return render(request, 'all_items.html', context)

def get_popular_items(request):
	items = GET_ITEMS()
	data = []

	for item in items:
		itemData = {
			'name': item.name,
			'cost': float(item.cost),
			'units_available': item.units_available,
			'details': item.details,
			'sale_start': str(item.sale_start),
			'sale_end': str(item.sale_end),
			'discount_start': str(item.discount_start),
			'discount_end': str(item.discount_end),
			'images': []
		}
		
		for img in ItemImage.objects.filter(item=item):
			itemData['images'].append({
				'url': img.file.url,
				'alt': img.alt
			})

		data.append(itemData)
	
	if data:
		return HttpResponse(json.dumps(data))
	else:
		return HttpResponse(status=404)

def search_items(request, keyword):
	print(keyword)
	items = Item.objects.all()
	data = []

	for item in items:
		if item.name.lower().startswith(keyword.lower()):
			itemData = {
				'name': item.name,
				'cost': float(item.cost),
				'units_available': item.units_available,
				'details': item.details,
				'sale_start': str(item.sale_start),
				'sale_end': str(item.sale_end),
				'discount_start': str(item.discount_start),
				'discount_end': str(item.discount_end),
				'images': []
			}
			
			for img in ItemImage.objects.filter(item=item):
				itemData['images'].append({
					'url': img.file.url,
					'alt': img.alt
				})

			data.append(itemData)
	
	if data:
		return HttpResponse(json.dumps(data))
	else:
		return HttpResponse(status=404)

@login_required
def account(request):
	user_items, num_user_items = GET_USER_ITEMS(request.user)

	context = {
		'username': request.user,
		'user_items': user_items,
		'num_user_items': num_user_items
	}

	return render(request, 'account/account.html', context)

@login_required
def user_items(request):
	user_items, num_user_items = GET_USER_ITEMS(request.user)

	context = {
		'user_items': user_items,
		'num_user_items': num_user_items
	}

	return render(request, 'account/user_items.html', context)

@login_required
def sales_data(request):
	items, num_user_items = GET_USER_ITEMS(request.user)

	user_items = []

	for item in items:
		revenue = item.units_sold * item.price
		cost = item.units_purchased * item.cost
		profit = revenue - cost
		
		user_items.append({
			'id': item.id,
			'name': item.name,
			'units_sold': item.units_sold,
			'revenue': revenue,
			'cost': cost,
			'profit': profit,
			'images': item.images
		})
	
	context = {
		'user_items': user_items,
		'num_user_items': num_user_items
	}

	return render(request, 'account/sales_data.html', context)

@login_required
def sales_info(request):
	return render(request, 'account/sales_info.html')

@login_required
def add_item(request):
	if request.method == 'POST' and request.user.is_authenticated:
		new_item_form = NewItemForm(request.POST)

		if new_item_form.is_valid():
			Item(
				user = request.user,
				name = new_item_form.cleaned_data.get('name'),
				cost = new_item_form.cleaned_data.get('cost'),
				price = new_item_form.cleaned_data.get('price'),
				units_available = new_item_form.cleaned_data.get('units_available'),
				sale_start = new_item_form.cleaned_data.get('sale_start'),
				sale_end = new_item_form.cleaned_data.get('sale_end'),
				discount_start = new_item_form.cleaned_data.get('discount_start'),
				discount_end = new_item_form.cleaned_data.get('discount_end'),
				details = new_item_form.cleaned_data.get('details')
			).save()

			return HttpResponseRedirect('/account/user_items/')
	else:
		new_item_form = NewItemForm()
	
	context = {
		'form': new_item_form
	}

	return render(request, 'account/add_item.html', context)

@login_required
def add_item_images(request, itemID):
	item = Item.objects.get(id=itemID)
	
	if request.user == item.user:
		if request.method == 'POST':
			new_image_form = NewImageForm(request.POST, request.FILES)

			if new_image_form.is_valid():
				ItemImage(
					item = item,
					file = new_image_form.cleaned_data.get('file'),
					alt = new_image_form.cleaned_data.get('alt')
				).save()
				
				return HttpResponseRedirect('/account/user_items/')
		else:
			new_image_form = NewImageForm()
	else:
		return HttpResponseRedirect('/account/')
	
	context = {
		'form': new_image_form,
		'item': item,
		'item_images': ItemImage.objects.filter(item=item)
	}

	return render(request, 'account/add_item_images.html', context)

@login_required
def delete_item(request, itemID):
	if request.method == 'POST':
		item = Item.objects.get(id=itemID)

		if item.user == request.user:
			item.delete()
			return HttpResponse(status=200)
		else:
			return HttpResponse(status=403)
	else:
		return HttpResponse(status=405)

@login_required
def contact_us(request):
	if request.method == 'POST':
		contact_form = ContactForm(request.POST)

		if contact_form.is_valid():
			try:
				send_mail(
					contact_form.cleaned_data.get('subject'),
					contact_form.cleaned_data.get('text'),
					request.user.email,
					[User.objects.get(username='admin').email]
				)

				success = 1
			except:
				success = 0

			context = {
				'form': ContactForm(),
				'success': success
			}
			
			return render(request, 'account/contact_us.html', context)
	else:
		contact_form = ContactForm()
	
	context = {
		'form': contact_form
	}

	return render(request, 'account/contact_us.html', context)

def register(request):
	if request.method == 'POST':
		reg_form = RegistrationForm(request.POST)

		if reg_form.is_valid():
			user = reg_form.save()
			user = authenticate(
				username = reg_form.cleaned_data.get('username'),
				password = reg_form.cleaned_data.get('password1')
			)

			login(request, user)
			return HttpResponseRedirect('/account/')
	else:
		reg_form = RegistrationForm()
	
	context = {
		'form': reg_form
	}
	
	return render(request, 'registration/register.html', context)