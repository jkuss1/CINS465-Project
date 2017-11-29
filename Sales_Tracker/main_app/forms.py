from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *

MONEY_PLACEHOLDER = "12.34"
DATETIME_FORMATS = ["%Y-%m-%d %H:%M"]
DATETIME_PLACEHOLDER = "YYYY-mm-dd HH:MM (24-Hour Time Format)"

class NewItemForm(forms.ModelForm):
	name = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'autofocus': True
			}
		)
	)

	cost = forms.DecimalField(
		widget = forms.NumberInput(
			attrs = {
				'placeholder': MONEY_PLACEHOLDER
			}
		)
	)

	price = forms.DecimalField(
		widget = forms.NumberInput(
			attrs = {
				'placeholder': MONEY_PLACEHOLDER
			}
		)
	)

	units_purchased = forms.IntegerField(
		widget = forms.NumberInput(
			attrs = {
				'placeholder': "0"
			}
		)
	)

	units_available = forms.IntegerField(
		widget = forms.NumberInput(
			attrs = {
				'placeholder': "0"
			}
		)
	)

	units_sold = forms.IntegerField(
		label = "Units Already Sold",
		widget = forms.NumberInput(
			attrs = {
				'placeholder': "0"
			}
		)
	)

	sale_start = forms.DateTimeField(
		input_formats = DATETIME_FORMATS,
		required = False,
		widget = forms.DateTimeInput(
			attrs = {
				'placeholder': DATETIME_PLACEHOLDER,
				'class': "auto-kal",
				'onchange': "dateChange(this)"
			}
		)
	)
	
	sale_end = forms.DateTimeField(
		input_formats = DATETIME_FORMATS,
		required = False,
		widget = forms.DateTimeInput(
			attrs = {
				'placeholder': DATETIME_PLACEHOLDER,
				'class': "auto-kal",
				'onchange': "dateChange(this)"
			}
		)
	)

	discount_start = forms.DateTimeField(
		input_formats = DATETIME_FORMATS,
		required = False,
		widget = forms.DateTimeInput(
			attrs = {
				'placeholder': DATETIME_PLACEHOLDER,
				'class': "auto-kal",
				'onchange': "dateChange(this)"
			}
		)
	)
	
	discount_end = forms.DateTimeField(
		input_formats = DATETIME_FORMATS,
		required = False,
		widget = forms.DateTimeInput(
			attrs = {
				'placeholder': DATETIME_PLACEHOLDER,
				'class': "auto-kal",
				'onchange': "dateChange(this)"
			}
		)
	)
	
	class Meta:
		model = Item
		exclude = ["user"]

class NewImageForm(forms.ModelForm):
	file = forms.ImageField(
		label = "Image"
	)

	alt = forms.CharField(
		label = "Description"
	)

	class Meta:
		model = ItemImage
		exclude = ["item"]

class ContactForm(forms.Form):
	subject = forms.CharField()

	text = forms.CharField(
		widget = forms.Textarea(
			attrs = {
				'placeholder': "Type your message here..."
			}
		)
	)

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(
		required = True
	)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")
	
	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		
		if commit:
			user.save()
		
		return user