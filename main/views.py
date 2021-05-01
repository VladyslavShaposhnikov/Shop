from django.shortcuts import render
from .models import Category
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

def index(request):
    return render(request, 'index.html', {
        'boys'  :boys,
        'girls' :girls,
        'baby'  :baby,
        'toys'  :toys,
        'sport' :sport,
        })

def show_categories(request):
    return render(request, "categories.html", {'categories':Category.objects.all(),
                                                'boys'     :boys,
                                                'girls'    :girls,
                                                'baby'     :baby,
                                                'toys'     :toys,
                                                'sport'    :sport,
                                                })