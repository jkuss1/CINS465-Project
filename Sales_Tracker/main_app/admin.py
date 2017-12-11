from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Item)

admin.site.register(
	ItemImage,
	list_display = ['alt', 'item']
)

admin.site.register(Cart)

admin.site.register(UserOnline)