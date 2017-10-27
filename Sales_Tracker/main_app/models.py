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
		null = True
	)
	
	price = models.DecimalField(
		max_digits = 12,
		decimal_places = 2,
		null = True
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