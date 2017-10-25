from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *

class NewItemForm(forms.ModelForm):
	img = forms.ImageField(
		label = "Image File"
	)

	imgDesc = forms.CharField(
		label = "Image Description"
	)

	class Meta:
		model = Item
		exclude = ["user"]
	
	def save(self, user, commit=True):
		item = super(NewItemForm, self).save(commit=False)
		item.user = user
		
		if commit:
			item.save()
		
		return item

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(
		label = "Email",
		required = True,
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

class LoginForm(AuthenticationForm):
	username = forms.CharField(
		label = "Username",
		max_length = 30,
		widget = forms.TextInput(
			attrs = {
				'class': "form-control",
				'name': "username"
			}
		)
	)

	password = forms.CharField(
		label = "Password",
		max_length = 32,
		widget = forms.PasswordInput()
	)