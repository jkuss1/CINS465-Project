from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Item)
admin.site.register(AccountSettings)

admin.site.register(
	ItemUnitSoldDate,
	list_display = ['item', 'date', 'amount']
)

admin.site.register(
	ItemImage,
	list_display = ['alt', 'item']
)