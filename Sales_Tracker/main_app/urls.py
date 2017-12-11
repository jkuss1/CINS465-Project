from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^register/$', views.register, name="register"),
	url(r'^all_items/$', views.all_items, name="all_items"),
	url(r'^get_popular_items/$', views.get_popular_items, name="get_popular_items"),
	url(r'^search_items/(?P<keyword>[\w]+)/$', views.search_items, name="search_items"),
	url(r'^account/$', views.account, name="account"),
	url(r'^account/add_item/$', views.add_item, name="add_item"),
	url(r'^account/add_item_images/(?P<itemID>[0-9]+)/$', views.add_item_images, name="add_item_images"),
	url(r'^account/delete_item/(?P<itemID>[0-9]+)/$', views.delete_item, name="delete_item"),
	url(r'^account/user_items/$', views.user_items, name="user_items"),
	url(r'^account/sales_data/$', views.sales_data, name="sales_data"),
	url(r'^account/sales_info/$', views.sales_info, name="sales_info"),
	url(r'^account/cart/$', views.cart, name="cart"),
	url(r'^account/add_to_cart/(?P<itemID>[0-9]+)/$', views.add_to_cart, name="add_to_cart"),
	url(r'^account/delete_from_cart/(?P<item_id>[0-9]+)/$', views.delete_from_cart, name="delete_from_cart"),
	url(r'^account/checkout/(?P<username>[\w]+)/$', views.checkout, name="checkout"),
	url(r'^account/receipt/(?P<username>[\w]+)/$', views.receipt, name="receipt"),
	url(r'^contact_us/$', views.contact_us, name="contact_us"),
	url(r'^send_email/(?P<item_id>[0-9]+)/$', views.send_email, name="send_email"),
]