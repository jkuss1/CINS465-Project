from django.shortcuts import render
from django.http import JsonResponse

from .models import *
from .forms import *

# Create your views here.
def index(request):
	context = {}
	
	return render(request, "default.html", context)