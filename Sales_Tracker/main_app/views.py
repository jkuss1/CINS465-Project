import json
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import *
from .forms import *

# CONSTANTS #
MONTH_NUM_TO_NAME = {
	1: 'Jan',
	2: 'Feb',
	3: 'Mar',
	4: 'Apr',
	5: 'May',
	6: 'Jun',
	7: 'Jul',
	8: 'Aug',
	9: 'Sep',
	10: 'Oct',
	11: 'Nov',
	12: 'Dec'
}

# FUNCTIONS #
def GET_FORMATTED_TIME(datetime_model):
	if datetime_model:
		utc = str(datetime_model).split(' ')
		
		date = utc[0].split("-")
		date = MONTH_NUM_TO_NAME[int(date[1])] + ". " + str(int(date[2])) + ", " + date[0] + ","
		
		time = utc[1].split(":")
		
		if int(time[1]) >= 12:
			am_pm = "p.m."
		else:
			am_pm = "a.m."
		
		time = time[0] + ":" + time[1] + " " + am_pm
		
		return date + " " + time
	else:
		return ""

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
		'username': request.user.username,
		'items': GET_ITEMS(0, 5),
		'user_items': user_items,
		'num_user_items': num_user_items
	}
	
	return render(request, 'index.html', context)

def all_items(request):
	context = {
		'username': request.user.username,
		'items': GET_ITEMS(),
		'seller_online': True
	}
	
	return render(request, 'all_items.html', context)

def get_popular_items(request):
	items = GET_ITEMS()
	data = []

	if request.user.is_authenticated:
		logged_in = "true"
	else:
		logged_in = ""

	for item in items:
		itemData = {
			'id': item.id,
			'name': item.name,
			'cost': float(item.cost),
			'unitsAvailable': item.units_available,
			'details': item.details,
			'saleStart': GET_FORMATTED_TIME(item.sale_start),
			'saleEnd': GET_FORMATTED_TIME(item.sale_end),
			'discountStart': GET_FORMATTED_TIME(item.discount_start),
			'discountEnd': GET_FORMATTED_TIME(item.discount_end),
			'images': [],
			'loggedIn': logged_in
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
	items = Item.objects.all()
	data = []

	if request.user.is_authenticated:
		logged_in = "true"
	else:
		logged_in = ""

	for item in items:
		if item.name.lower().startswith(keyword.lower()):
			itemData = {
				'id': item.id,
				'name': item.name,
				'cost': float(item.cost),
				'unitsAvailable': item.units_available,
				'details': item.details,
				'saleStart': GET_FORMATTED_TIME(item.sale_start),
				'saleEnd': GET_FORMATTED_TIME(item.sale_end),
				'discountStart': GET_FORMATTED_TIME(item.discount_start),
				'discountEnd': GET_FORMATTED_TIME(item.discount_end),
				'images': [],
				'loggedIn': logged_in
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
		'username': request.user.username,
		'user_items': user_items,
		'num_user_items': num_user_items
	}

	return render(request, 'account/account.html', context)

@login_required
def user_items(request):
	user_items, num_user_items = GET_USER_ITEMS(request.user)

	context = {
		'username': request.user.username,
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
		'username': request.user.username,
		'user_items': user_items,
		'num_user_items': num_user_items
	}

	return render(request, 'account/sales_data.html', context)

@login_required
def sales_info(request):
	items = Item.objects.filter(user=request.user)
	
	items_sold = items.order_by('-units_sold')
	highest_selling_items = []
	
	if len(items_sold) > 1:
		for i in range(0, len(items_sold)):
			if i + 1 < len(items_sold):
				if items_sold[i].units_sold > items_sold[i + 1].units_sold:
					highest_selling_items.append(items_sold[i])
				else:
					highest_selling_items.append(items_sold[i + 1])
	elif len(items_sold) == 1:
		highest_selling_items.append(items_sold[0])
	
	context = {
		'highest_selling_items': highest_selling_items
	}

	return render(request, 'account/sales_info.html', context)

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
		'username': request.user.username,
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
		'username': request.user.username,
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
def cart(request):
	cart_item_ids = request.user.cart.item_ids.split(',')
	items = []
	num_items_in_cart = 0

	for cart_item_id in cart_item_ids:
		if cart_item_id:
			num_items_in_cart = num_items_in_cart + 1
			items.append(Item.objects.get(id=cart_item_id))
	
	context = {
		'username': request.user.username,
		'items': items,
		'num_items_in_cart': num_items_in_cart
	}

	return render(request, 'account/cart.html', context)

@login_required
def checkout(request):
	if request.method == 'POST':
		cart = request.user.cart
		item_ids = cart.item_ids.split(",")
		items = []

		for cart_item_id in item_ids:
			if cart_item_id:
				items.append(Item.objects.get(id=cart_item_id))
		
		cart.item_ids = ""
		cart.save()
		
		context = {
			'username': request.user.username,
			'items': items
		}
		
		return render(request, 'account/checkout.html', context)
	else:
		return HttpResponse(status=405)

@login_required
def add_to_cart(request, itemID):
	if request.method == 'POST':
		cart = request.user.cart
		item_ids = cart.item_ids.split(',')
		
		for cart_item_id in item_ids:
			if itemID == cart_item_id:
				return HttpResponse(status=200)
		
		if cart.item_ids == "":
			cart.item_ids = cart.item_ids + itemID
		else:
			cart.item_ids = cart.item_ids + "," + itemID
		
		cart.save()
		
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=405)

@login_required
def delete_from_cart(request, item_id):
	if request.method == 'POST':
		cart = request.user.cart

		if cart.user == request.user:
			if cart.item_ids.find("," + item_id + ",") != -1:
				cart.item_ids = cart.item_ids.replace("," + item_id, "")
			elif cart.item_ids.find(item_id + ",") != -1:
				cart.item_ids = cart.item_ids.replace(item_id + ",", "")
			elif cart.item_ids.find("," + item_id) != -1:
				cart.item_ids = cart.item_ids.replace("," + item_id, "")
			else:
				cart.item_ids = cart.item_ids.replace(item_id, "")
			
			cart.save()
			
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
				'username': request.user.username,
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
			
			Cart.objects.create(
				user = user
			)
			
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