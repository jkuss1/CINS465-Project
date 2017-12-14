from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def UserDirectoryPath(instance, filename):
	return "{0}/{1}/{2}".format(
		instance.item.user.id,
		instance.item.id,
		filename
	)

class Item(models.Model):
	user = models.ForeignKey(
		User,
		on_delete = models.CASCADE,
		null = True
	)
	
	name = models.CharField(
		max_length = 32
	)

	cost = models.DecimalField(
		max_digits = 12,
		decimal_places = 2,
		default = 0.00
	)
	
	price = models.DecimalField(
		max_digits = 12,
		decimal_places = 2,
		default = 0.00
	)

	units_purchased = models.IntegerField(
		default = 0
	)

	units_available = models.IntegerField(
		default = 0
	)

	units_previously_sold = models.IntegerField(
		default = 0
	)

	units_sold = models.IntegerField(
		default = 0
	)

	sale_start = models.DateTimeField(
		null = True,
		blank = True
	)
	
	sale_end = models.DateTimeField(
		null = True,
		blank = True
	)

	discount_start = models.DateTimeField(
		null = True,
		blank = True
	)
	
	discount_end = models.DateTimeField(
		null = True,
		blank = True
	)
	
	details = models.TextField()
	
	date_created = models.DateTimeField(
		auto_now_add = True
	)

	date_updated = models.DateTimeField(
		auto_now = True
	)

	def __str__(self):
		return self.name

class ItemUnitSoldDate(models.Model):
	item = models.ForeignKey(
		Item,
		on_delete = models.CASCADE,
	)

	amount = models.IntegerField(
		default = 0
	)

	date = models.DateField(
		auto_now_add = True
	)

	def __str__(self):
		return self.item.name

class ItemImage(models.Model):
	item = models.ForeignKey(
		Item,
		on_delete = models.CASCADE
	)

	file = models.ImageField(
		upload_to = UserDirectoryPath
	)

	alt = models.CharField(
		max_length = 32
	)

	def __str__(self):
		return self.alt

class AccountSettings(models.Model):
	user = models.OneToOneField(
		User,
		related_name = "settings",
		on_delete = models.CASCADE
	)
	
	deny_chat = models.BooleanField()
	
	cart = models.TextField(
		null = True,
		blank = True
	)
	
	online = models.BooleanField()
	
	def __str__(self):
		return self.user.username