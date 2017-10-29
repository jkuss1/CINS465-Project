from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *

MONEY_PLACEHOLDER = "12.34"

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