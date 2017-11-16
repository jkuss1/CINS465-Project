from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^register/$', views.register, name="register"),
	url(r'^account/$', views.account, name="account"),
	url(r'^account/add_item/$', views.add_item, name="add_item"),
	url(r'^account/add_item_images/(?P<itemID>[0-9]+)/$', views.add_item_images, name="add_item_images"),
	url(r'^account/user_items/$', views.user_items, name="user_items"),
	url(r'^account/sales_data/$', views.sales_data, name="sales_data"),
	url(r'^account/sales_info/$', views.sales_info, name="sales_info"),
	url(r'^account/contact_us/$', views.contact_us, name="contact_us"),
]