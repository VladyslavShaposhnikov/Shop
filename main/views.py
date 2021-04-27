from django.shortcuts import render
from .models import Category

def index(request):
    return render(request, 'index.html')

def show_categories(request):
    return render(request, "categories.html", {'categories': Category.objects.all()})