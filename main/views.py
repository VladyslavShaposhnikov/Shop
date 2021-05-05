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

def productdetail(request,slug):
    product = BoyGirlBaby.objects.get(slug=slug)
    return render(request, 'product_detaile.html', {'product':product,
                                                    'boys'   :boys,
                                                    'girls'  :girls,
                                                    'baby'   :baby,
                                                    'toys'   :toys,
                                                    'sport'  :sport,
                                                })

def categorydetail(request,slug):
    category = Category.objects.get(slug=slug)
    return render(request, 'category_detail.html', {'category':category,
                                                    'boys'   :boys,
                                                    'girls'  :girls,
                                                    'baby'   :baby,
                                                    'toys'   :toys,
                                                    'sport'  :sport,
                                                })