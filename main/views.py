from django.shortcuts import render
from .models import Category, Boy, Baby, Girl, Toys, Sport
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

GET_MODEL_SLUG = {
    'boy':Boy,
    'girl':Girl,
    'baby':Baby,
    'toys':Toys,
    'sport':Sport
}

def index(request):
    return render(request, 'index.html', context)

def show_categories(request):
    context['categories'] = Category.objects.all()
    return render(request, "categories.html", context)

def boyproductdetail(request,slug):
    context['product'] = Boy.objects.get(slug=slug)
    return render(request, 'product_detaile.html', context)

def girlproductdetail(request,slug):
    context['product'] = Girl.objects.get(slug=slug)
    return render(request, 'product_detaile.html', context)

def babyproductdetail(request,slug):
    context['product'] = Baby.objects.get(slug=slug)
    return render(request, 'product_detaile.html', context)

def categorydetail(request,slug):
    context['category'] = Category.objects.get(slug=slug)
    return render(request, 'category_detail.html', context)