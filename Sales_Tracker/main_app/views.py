import json
from datetime import datetime

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

def GET_ONLINE_USERS(items):
	sellers_online = []

	for item in items:
		sellers_online.append((item.id, item.user.settings.online, item.user.settings.deny_chat))
	
	return sellers_online

# VIEWS #
def index(request):
	items = GET_ITEMS(0, 5)
	
	context = {
		'items': items,
		'sellers_online': GET_ONLINE_USERS(items)
	}
	
	return render(request, 'index.html', context)

def all_items(request):
	items = GET_ITEMS()
	
	context = {
		'items': items,
		'sellers_online': GET_ONLINE_USERS(items)
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
			'seller': item.user.username,
			'price': str(float(item.price)),
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
				'seller': item.user.username,
				'price': str(float(item.price)),
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
	if request.method == 'POST':
		account_settings_form = AccountSettingsForm(request.POST)
		
		if account_settings_form.is_valid():
			request.user.settings.deny_chat = account_settings_form.cleaned_data['deny_chat']
			request.user.settings.save()
			
			return HttpResponseRedirect('/account/')
	else:
		account_settings_form = AccountSettingsForm()
	
	context = {
		'form': account_settings_form
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

		dates_sold = ItemUnitSoldDate.objects.filter(item=item)
		months = {}
		
		for date_sold in dates_sold:
			month = str(date_sold.date).split("-")[1]

			if not months.get(month):
				months[month] = date_sold.amount
			else:
				months[month] = months[month] + date_sold.amount
		
		most_popular_month = None
		most_popular_month_amount = -1
		least_popular_month = None
		least_popular_month_amount = float('inf')

		for month in months:
			month = int(month)

			if month > most_popular_month_amount:
				most_popular_month = MONTH_NUM_TO_NAME[month] + "."
			
			if month < least_popular_month_amount:
				least_popular_month = MONTH_NUM_TO_NAME[month] + "."
		
		user_items.append({
			'id': item.id,
			'name': item.name,
			'units_sold': item.units_sold,
			'most_popular_month': most_popular_month,
			'least_popular_month': least_popular_month,
			'revenue': revenue,
			'cost': cost,
			'profit': profit
		})
	
	context = {
		'user_items': user_items,
		'num_user_items': num_user_items
	}

	return render(request, 'account/sales_data.html', context)

@login_required
def sales_info(request):
	items = Item.objects.filter(user=request.user)

	total_units_sold = 0
	total_cost = 0
	total_revenue = 0
	months = {}
	
	for item in items:
		total_units_sold = total_units_sold + item.units_sold
		total_cost = total_cost + (item.cost * item.units_purchased)
		total_revenue = total_revenue + (item.price * item.units_sold)

		dates_sold = ItemUnitSoldDate.objects.filter(item=item)
		for date_sold in dates_sold:
			month = str(date_sold.date).split('-')[1]
			if not months.get(month):
				months[month] = (item.price - item.cost) * date_sold.amount
			else:
				months[month] = months[month] + ((item.price - item.cost) * date_sold.amount)
	
	most_profitable_months = []
	most_profitable_month_amount = -1
	least_profitable_months = []
	least_profitable_month_amount = float('inf')
	for month, profit in months.items():
		if profit > most_profitable_month_amount:
			most_profitable_months = []
			most_profitable_months.append(MONTH_NUM_TO_NAME[int(month)] + ".")
			most_profitable_month_amount = profit
		elif profit == most_profitable_month_amount:
			most_profitable_months.append(MONTH_NUM_TO_NAME[int(month)] + ".")
		if profit < least_profitable_month_amount:
			least_profitable_months = []
			least_profitable_months.append(MONTH_NUM_TO_NAME[int(month)] + ".")
			least_profitable_month_amount = profit
		elif profit == least_profitable_month_amount:
			least_profitable_months.append(MONTH_NUM_TO_NAME[int(month)] + ".")
	
	highest_selling_items = items.order_by('-units_sold')
	highest_selling_items_range = 1
	for i in range(0, len(highest_selling_items)):
		if i + 1 < len(highest_selling_items):
			if highest_selling_items[i + 1].units_sold == highest_selling_items[i].units_sold:
				highest_selling_items_range = highest_selling_items_range + 1
			else:
				break
		else:
			break
	
	lowest_selling_items = items.order_by('units_sold')
	lowest_selling_items_range = 1
	for i in range(0, len(lowest_selling_items)):
		if i + 1 < len(lowest_selling_items):
			if lowest_selling_items[i + 1].units_sold == lowest_selling_items[i].units_sold:
				lowest_selling_items_range = lowest_selling_items_range + 1
			else:
				break
		else:
			break
	
	most_expensive_items = items.order_by('-price')
	most_expensive_items_range = 1
	for i in range(0, len(most_expensive_items)):
		if i + 1 < len(most_expensive_items):
			if most_expensive_items[i + 1].price == most_expensive_items[i].price:
				most_expensive_items_range = most_expensive_items_range + 1
			else:
				break
		else:
			break
	
	cheapest_items = items.order_by('price')
	cheapest_items_range = 1
	for i in range(0, len(cheapest_items)):
		if i + 1 < len(cheapest_items):
			if cheapest_items[i + 1].price == cheapest_items[i].price:
				cheapest_items_range = cheapest_items_range + 1
			else:
				break
		else:
			break
	
	most_profitable_items = []
	most_profitable_items_amount = -1
	least_profitable_items = []
	least_profitable_items_amount = float('inf')
	for item in items:
		profit = item.price - item.cost
		if profit > most_profitable_items_amount:
			most_profitable_items = []
			most_profitable_items.append(item)
			most_profitable_items_amount = profit
		elif profit == most_profitable_items_amount:
			most_profitable_items.append(item)
		if profit < least_profitable_items_amount:
			least_profitable_items = []
			least_profitable_items.append(item)
			least_profitable_items_amount = profit
		elif profit == least_profitable_items_amount:
			least_profitable_items.append(item)
	
	context = {
		'total_units_sold': total_units_sold,
		'total_cost': total_cost,
		'total_revenue': total_revenue,
		'total_profit': total_revenue - total_cost,
		'highest_selling_items': highest_selling_items[:highest_selling_items_range],
		'lowest_selling_items': lowest_selling_items[:lowest_selling_items_range],
		'most_expensive_items': most_expensive_items[:most_expensive_items_range],
		'cheapest_items': cheapest_items[:cheapest_items_range],
		'most_profitable_items': most_profitable_items,
		'least_profitable_items': least_profitable_items,
		'most_profitable_months': most_profitable_months,
		'least_profitable_months': least_profitable_months
	}

	return render(request, 'account/sales_info.html', context)

@login_required
def add_item(request):
	if request.method == 'POST' and request.user.is_authenticated:
		new_item_form = ItemForm(request.POST)

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
		new_item_form = ItemForm()
	
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
def edit_item(request, item_id):
	item = Item.objects.filter(id=item_id)

	if item:
		item = item[0]
		item_data = ""
		
		if request.user == item.user:
			if request.method == 'POST':
				edit_item_form = ItemForm(request.POST)

				if edit_item_form.is_valid():
					item.name = edit_item_form.cleaned_data['name']
					item.cost = edit_item_form.cleaned_data['cost']
					item.price = edit_item_form.cleaned_data['price']
					item.units_purchased = edit_item_form.cleaned_data['units_purchased']
					item.units_available = edit_item_form.cleaned_data['units_available']
					item.units_previously_sold = edit_item_form.cleaned_data['units_previously_sold']
					item.sale_start = edit_item_form.cleaned_data['sale_start']
					item.sale_end = edit_item_form.cleaned_data['sale_end']
					item.discount_start = edit_item_form.cleaned_data['discount_start']
					item.discount_end = edit_item_form.cleaned_data['discount_end']
					item.details = edit_item_form.cleaned_data['details']
					item.save()
					
					return HttpResponseRedirect('/account/user_items/')
			else:
				edit_item_form = ItemForm()

				item_data = json.dumps({
					'name': item.name,
					'cost': str(float(item.cost)),
					'price': str(float(item.price)),
					'units_purchased': item.units_purchased,
					'units_available': item.units_available,
					'units_previously_sold': item.units_previously_sold,
					'sale_start': str(item.sale_start),
					'sale_end': str(item.sale_end),
					'discount_start': str(item.discount_start),
					'discount_end': str(item.discount_end),
					'details': item.details
				})
			
			context = {
				'form': edit_item_form,
				'item': item,
				'item_data': item_data
			}

			return render(request, 'account/edit_item.html', context)
	else:
		return HttpResponseRedirect('/')

@login_required
def delete_item(request, item_id):
	if request.method == 'POST':
		item = Item.objects.get(id=item_id)

		if item.user == request.user:
			item.delete()
			return HttpResponse(status=200)
		else:
			return HttpResponse(status=403)
	else:
		return HttpResponse(status=405)

@login_required
def cart(request):
	user_settings = request.user.settings
	items = []
	num_items_in_cart = 0
	
	if user_settings.cart:
		cart_item_ids = user_settings.cart.split(',')
		
		for cart_item_id in cart_item_ids:
			if cart_item_id:
				item = Item.objects.filter(id=cart_item_id)
				
				if item:
					num_items_in_cart = num_items_in_cart + 1
					items.append(item[0])
	
	context = {
		'items': items,
		'num_items_in_cart': num_items_in_cart
	}

	return render(request, 'account/cart.html', context)

@login_required
def add_to_cart(request, itemID):
	if request.method == 'POST':
		user_settings = request.user.settings
		
		if user_settings.cart:
			item_ids = user_settings.cart.split(',')
			
			for cart_item_id in item_ids:
				if itemID == cart_item_id:
					return HttpResponse(status=200)
		
		if not user_settings.cart or user_settings.cart == "":
			user_settings.cart = itemID
		else:
			user_settings.cart = user_settings.cart + "," + itemID
		
		user_settings.save()
		
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=405)

@login_required
def delete_from_cart(request, item_id):
	if request.method == 'POST':
		user_settings = request.user.settings

		if user_settings.user == request.user:
			if user_settings.cart.find("," + item_id + ",") != -1:
				user_settings.cart = user_settings.cart.replace("," + item_id, "")
			elif user_settings.cart.find(item_id + ",") != -1:
				user_settings.cart = user_settings.cart.replace(item_id + ",", "")
			elif user_settings.cart.find("," + item_id) != -1:
				user_settings.cart = user_settings.cart.replace("," + item_id, "")
			else:
				user_settings.cart = user_settings.cart.replace(item_id, "")
			
			user_settings.save()
			
			return HttpResponse(status=200)
		else:
			return HttpResponse(status=403)
	else:
		return HttpResponse(status=405)

@login_required
def checkout(request, username):
	if request.method == 'POST':
		if request.user.username == username:
			user_settings = request.user.settings
			item_ids = user_settings.cart.split(",")
			
			for cart_item_id in item_ids:
				if cart_item_id:
					item = Item.objects.get(id=cart_item_id)
					item.units_sold = item.units_sold + 1
					
					dates_sold = ItemUnitSoldDate.objects.filter(item=item)

					if dates_sold:
						for date_sold in dates_sold:
							if str(date_sold.date) == str(datetime.now()).split(" ")[0]:
								date_sold.amount = date_sold.amount + 1
								date_sold.save()
								break
					else:
						ItemUnitSoldDate.objects.create(
							item = item,
							amount = 1
						)
					
					item.save()
			
			return HttpResponseRedirect('/account/receipt/' + username)
		else:
			return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/')

@login_required
def receipt(request, username):
	if request.user.username == username:
		user_settings = request.user.settings
		item_ids = user_settings.cart.split(",")
		items = []

		for cart_item_id in item_ids:
			if cart_item_id:
				items.append(Item.objects.get(id=cart_item_id))
		
		user_settings.cart = ""
		user_settings.save()
		
		context = {
			'items': items
		}

		return render(request, 'account/receipt.html', context)
	else:
		return HttpResponseRedirect('/')

@login_required
def send_email(request, item_id):
	item = Item.objects.get(id=item_id)
	
	if request.method == 'POST':
		email_form = EmailForm(request.POST)

		if email_form.is_valid():
			try:
				send_mail(
					email_form.cleaned_data.get('subject'),
					email_form.cleaned_data.get('text'),
					request.user.email,
					[item.user.email]
				)

				success = 1
			except:
				success = 0
			
			if success == 1:
				return HttpResponseRedirect('/all_items/')
			else:
				context = {
					'item': item,
					'form': EmailForm(),
					'success': success
				}

				return render(request, 'email_seller.html', context)
	else:
		email_form = EmailForm()
	
	context = {
		'form': email_form,
		'item': item
	}
	
	return render(request, 'email_seller.html', context)

@login_required
def contact_us(request):
	if request.method == 'POST':
		email_form = EmailForm(request.POST)

		if email_form.is_valid():
			try:
				send_mail(
					email_form.cleaned_data.get('subject'),
					email_form.cleaned_data.get('text'),
					request.user.email,
					[User.objects.get(username='admin').email]
				)

				success = 1
			except:
				success = 0

			context = {
				'form': EmailForm(),
				'success': success
			}
			
			return render(request, 'contact_us.html', context)
	else:
		email_form = EmailForm()
	
	context = {
		'form': email_form
	}

	return render(request, 'contact_us.html', context)

def register(request):
	if request.method == 'POST':
		reg_form = RegistrationForm(request.POST)

		if reg_form.is_valid():
			user = reg_form.save()
			
			AccountSettings.objects.create(
				user = user,
				deny_chat = False,
				online = True
			)
			
			user = authenticate(
				username = reg_form.cleaned_data.get('username'),
				password = reg_form.cleaned_data.get('password1')
			)

			login(request, user)
			return HttpResponseRedirect('/')
	else:
		reg_form = RegistrationForm()
	
	context = {
		'form': reg_form
	}
	
	return render(request, 'registration/register.html', context)