from django.conf.urls import url
from firstapp.views import HomePage
from firstapp.views import CalcPage
from firstapp.views import InputPage
from firstapp.views import SalesPage
from firstapp.views import InfoPage

urlpatterns = [
	url(r'^$', HomePage.as_view(), name='home'),
	url(r'calc$', CalcPage.as_view(), name='calc'),
	url(r'input$', InputPage.as_view(), name='input'),
	url(r'sales$', SalesPage.as_view(), name='sales'),
	url(r'info$', InfoPage.as_view(), name='info'),
]

