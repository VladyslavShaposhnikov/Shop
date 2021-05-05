from django.shortcuts import render
from .models import Category, BoyGirlBaby
from django.views.generic.detail import DetailView

def get_cat(num):
    cat = Category.objects.get(pk=num)
    cats = cat.get_children()
    return cats

boys = get_cat(5)
girls = get_cat(2)
baby = get_cat(9)
toys = get_cat(10)
sport = get_cat(11)

context = {
    'boys'  :boys,
    'girls' :girls,
    'baby'  :baby,
    'toys'  :toys,
    'sport' :sport,
}

def index(request):
    return render(request, 'index.html', context)

def show_categories(request):
    context['categories'] = Category.objects.all()
    return render(request, "categories.html", context)

def productdetail(request,slug):
    context['product'] = BoyGirlBaby.objects.get(slug=slug)
    return render(request, 'product_detaile.html', context)

def categorydetail(request,slug):
    context['category'] = Category.objects.get(slug=slug)
    return render(request, 'category_detail.html', context)