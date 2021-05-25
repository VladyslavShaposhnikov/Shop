from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect

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
    context['babies'] = Baby.objects.filter(father=None).order_by('-pub_date')
    cart_owner = Customer.objects.get(user=request.user)
    context['cart'] = Cart.objects.get(customer=cart_owner)
    return render(request, 'index.html', context)

def show_categories(request):
    context['categories'] = Category.objects.all()
    return render(request, "categories.html", context)

class Productdetail(DetailView):
    
    GET_MODEL_SLUG = {
    'boy':Boy,
    'girl':Girl,
    'baby':Baby,
    'toys':Toys,
    'sport':Sport
}
    def dispatch(self, request, *args, **kwargs):
        self.model = self.GET_MODEL_SLUG[kwargs['ct_model']]
        self.queryset = self.model.objects.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detaile.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['boys'] = boys
        context['girls'] = girls
        context['baby'] = baby
        context['toys'] = toys
        context['sport'] = sport
        cart_owner = Customer.objects.get(user=self.request.user)
        context['cart'] = Cart.objects.get(customer=cart_owner)
        context['size_of_prod'] = self.model.objects.get(slug=self.kwargs['slug'])
        return context

Boys = ('shoes','blouse', 'jacket', 'underwear', 'socks', 'reglan', 'sportswear', 't-short', 'hat', 'pants')
Girls = ('shoes-for-girl','blouse-for-girl', 'jacket-for-girl', 'dress', 'underwear-for-girl', 'reglan-for-girl', 'sportswear-for-girl', 't-short-for-girl', 'hat-for-girl', 'pants-for-girl', 'tights-for-girl')
Toy = ('for-girls', 'for-boys', 'constructors', 'stuffed-animals', 'musical-toys', 'board-games', 'educational-toys')
Spor = ('cycling', 'skateboards', 'sled', 'scooters')

def categorydetail(request,slug):
    context['category'] = Category.objects.get(slug=slug)
    if slug in Boys:
        context['cats'] = Boy.objects.filter(father=None, category__slug=slug)
    elif slug in Girls:
        context['cats'] = Girl.objects.filter(father=None, category__slug=slug)
    elif slug in Toy:
        context['cats'] = Toys.objects.filter(category__slug=slug)
    elif slug in Spor:
        context['cats'] = Sport.objects.filter(category__slug=slug)
    else:
        context['cats'] = Baby.objects.filter(father=None, category__slug=slug)
    cart_owner = Customer.objects.get(user=request.user)
    context['cart'] = Cart.objects.get(customer=cart_owner)
    return render(request, 'category_detail.html', context)

def cart(request):
    cart_owner = Customer.objects.get(user=request.user)
    context['cart'] = Cart.objects.get(customer=cart_owner)
    context['baby_size'] = Baby.objects.all()
    context['boy_size'] = Boy.objects.all()
    context['girl_size'] = Girl.objects.all()
    return render(request, 'cart.html', context)

def add_to_cart(request, *args, **kwargs):
    ct_model, slug = kwargs.get('ct_model'), kwargs.get('slug')
    cart_owner = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(customer=cart_owner, in_order=False)
    prod = Product.objects.get(slug=slug)
    cart_prod, created = CartProduct.objects.get_or_create(
        owner=cart_owner,
        basket=cart,
        product=prod
    )
    if created:
        cart.product_in_cart.add(cart_prod)
        messages.add_message(request, messages.INFO, "'{}' додано до кошику".format(prod.title))
    else:
        messages.add_message(request, messages.INFO, "'{}' вже є у вашому кошику".format(prod.title))
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), context)

def delete_from_cart(request, *args, **kwargs):
    ct_model, slug = kwargs.get('ct_model'), kwargs.get('slug')
    cart_owner = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(customer=cart_owner, in_order=False)
    prod = Product.objects.get(slug=slug)
    cart_prod = CartProduct.objects.get(
        owner=cart_owner,
        basket=cart,
        product=prod
    )
    cart.product_in_cart.remove(cart_prod)
    cart_prod.delete()
    cart.save()
    messages.add_message(request, messages.INFO, "'{}' видалено з кошику".format(prod.title))
    return HttpResponseRedirect('/cart', context)

def change_qty_cartproduct(request, *args, **kwargs):
    ct_model, slug = kwargs.get('ct_model'), kwargs.get('slug')
    cart_owner = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(customer=cart_owner, in_order=False)
    prod = Product.objects.get(slug=slug)
    cart_prod = CartProduct.objects.get(
        owner=cart_owner,
        basket=cart,
        product=prod
    )
    num = int(request.POST.get('qty'))
    cart_prod.qty = num
    cart_prod.save()
    cart.save()
    messages.add_message(request, messages.INFO, "Ви змінили кількість '{}' на '{}'".format(prod.title, num))
    return HttpResponseRedirect('/cart', context)

def searching(request):
    search_query = request.GET.get('search1', '')
    if search_query:
        context['babies'] = Baby.objects.filter(title__contains=search_query).filter(father=None)
        context['b'] = Boy.objects.filter(title__contains=search_query).filter(father=None)
        context['g'] = Girl.objects.filter(title__contains=search_query).filter(father=None)
        context['t'] = Toys.objects.filter(title__contains=search_query)
        context['s'] = Sport.objects.filter(title__contains=search_query)
    else:
        context['babies'] = Baby.objects.filter(father=None).order_by('-pub_date')
    return render(request,'search_temp.html', context)