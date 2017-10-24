from django.conf.urls import url
from main_app.views import CalcPage
from main_app.views import InputPage
from main_app.views import SalesPage
from main_app.views import InfoPage

from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'register/$', views.register, name="register"),
	url(r'account/$', views.account, name="account"),
	url(r'calc$', CalcPage.as_view(), name='calc'),
	url(r'input$', InputPage.as_view(), name='input'),
	url(r'sales$', SalesPage.as_view(), name='sales'),
	url(r'info$', InfoPage.as_view(), name='info'),
]