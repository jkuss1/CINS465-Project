from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'register/$', views.register, name="register"),
	url(r'account/$', views.account, name="account"),
	url(r'account/add_item/$', views.add_item, name="add_item"),
	url(r'account/add_item_images/(?P<itemID>[0-9]+)/$', views.add_item_images, name="add_item_images"),
]