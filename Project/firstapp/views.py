from django.shortcuts import render, redirect
from django.views.generic import TemplateView

class HomePage(TemplateView):
	template_name = 'home/home.html'

class CalcPage(TemplateView):
	template_name = 'calc/calc.html'
	
class InputPage(TemplateView):
	template_name = 'input/input.html'
	
class SalesPage(TemplateView):
	template_name = 'sales/sales.html'
	
class InfoPage(TemplateView):
	template_name = 'info/info.html'