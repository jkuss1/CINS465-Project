from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'register/$', views.register, name="register"),
	url(r'account/$', views.account, name="account"),
	url(r'account/add_item/$', views.add_item, name="add_item"),
]