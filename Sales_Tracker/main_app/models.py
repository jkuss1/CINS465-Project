from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def UserDirectoryPath(instance, filename):
	return "{0} - {1}/{2}/{3}".format(
		instance.user.id,
		instance.user.username,
		instance.name,
		filename
	)

class Item(models.Model):
	user = models.ForeignKey(
		User,
		on_delete = models.CASCADE,
		null = True,
		blank = True
	)
	
	name = models.CharField(
		max_length = 32
	)

	details = models.TextField()

	img = models.ImageField(
		upload_to = UserDirectoryPath,
		null = True,
		blank = True
	)

	imgDesc = models.CharField(
		max_length = 32,
		null = True,
		blank = True
	)

	dateAdded = models.DateTimeField(
		auto_now_add = True
	)

	dateLastUpdated = models.DateTimeField(
		auto_now = True
	)

	def __str__(self):
		return self.name