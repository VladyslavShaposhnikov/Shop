from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import View
from django.http import HttpResponseRedirect
from .forms import OrderForm

def get_cat(num):
    cat = Category.objects.get(pk=num)
    cats = cat.get_children()
    return cats

boys = get_cat(5)
girls = get_cat(2)
baby = get_cat(9)
toys = get_cat(10)
sport = get_cat(11)

def user_cart(cus):
    if cus.is_authenticated:
        customer = Customer.objects.filter(user=cus).first()
        if not customer:
            customer = Customer.objects.create(user=cus)
        cart = Cart.objects.filter(customer=customer, in_order=False)
        if cart:
            cart = cart.get()
            return cart
        else:
            cart = Cart.objects.create(customer=customer)
            return cart 
    else:
        cart = Cart.objects.filter(for_anonymous_user=True).first()
        if cart:
            #cart = cart.get()
            return cart
        else:
            cart = Cart.objects.create(for_anonymous_user=True)
            return cart

context = {
    'boys'  : boys,
    'girls' : girls,
    'baby'  : baby,
    'toys'  : toys,
    'sport' : sport,
    } 

def index(request):
    context['babies'] = Baby.objects.filter(father=None).order_by('-pub_date')
    cus = request.user
    c = user_cart(cus)
    print(cus, c)
    context['cart'] = c
    #context['cart'] = Cart.objects.get(customer=cart_owner)
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
        cus = self.request.user
        c = user_cart(cus)
        context['cart'] = c
        context['size_of_prod'] = self.model.objects.get(slug=self.kwargs['slug'])
        return context

Boys_category_slug = ('shoes','blouse', 'jacket', 'underwear', 'socks', 'reglan', 'sportswear', 't-short', 'hat', 'pants')
Girls_category_slug = ('shoes-for-girl','blouse-for-girl', 'jacket-for-girl', 'dress', 'underwear-for-girl', 'reglan-for-girl', 'sportswear-for-girl', 't-short-for-girl', 'hat-for-girl', 'pants-for-girl', 'tights-for-girl')
Toys_category_slug = ('for-girls', 'for-boys', 'constructors', 'stuffed-animals', 'musical-toys', 'board-games', 'educational-toys')
Sport_category_slug = ('cycling', 'skateboards', 'sled', 'scooters')

def categorydetail(request,slug):
    context['category'] = Category.objects.get(slug=slug)
    if slug in Boys_category_slug:
        context['cats'] = Boy.objects.filter(father=None, category__slug=slug)
    elif slug in Girls_category_slug:
        context['cats'] = Girl.objects.filter(father=None, category__slug=slug)
    elif slug in Toys_category_slug:
        context['cats'] = Toys.objects.filter(category__slug=slug)
    elif slug in Sport_category_slug:
        context['cats'] = Sport.objects.filter(category__slug=slug)
    else:
        context['cats'] = Baby.objects.filter(father=None, category__slug=slug)
    cus = request.user
    c = user_cart(cus)
    context['cart'] = c
    return render(request, 'category_detail.html', context)

def cart(request):
    cus = request.user
    c = user_cart(cus)
    context['cart'] = c
    context['baby_size'] = Baby.objects.all()
    context['boy_size'] = Boy.objects.all()
    context['girl_size'] = Girl.objects.all()
    return render(request, 'cart.html', context)

def add_to_cart(request, *args, **kwargs):
    ct_model, slug = kwargs.get('ct_model'), kwargs.get('slug')
    cus = request.user
    c = user_cart(cus)
    prod = Product.objects.get(slug=slug)
    cart_prod, created = CartProduct.objects.get_or_create(
        owner=c.customer,
        basket=c,
        product=prod
    )
    if created:
        c.product_in_cart.add(cart_prod)
        messages.add_message(request, messages.INFO, "'{}' додано до кошику".format(prod.title))
    else:
        messages.add_message(request, messages.INFO, "'{}' вже є у вашому кошику".format(prod.title))
    recalculate_cart(c)
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
    recalculate_cart(cart)
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
    recalculate_cart(cart)
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

def about_us(request):
    cus = request.user
    c = user_cart(cus)
    context['cart'] = c
    return render(request, 'about_us.html', context)

def contacts(request):
    cus = request.user
    c = user_cart(cus)
    context['cart'] = c
    return render(request, 'contact.html', context)

def checkout(request):
    cus = request.user
    c = user_cart(cus)
    context['cart'] = c
    context['baby_size'] = Baby.objects.all()
    context['boy_size'] = Boy.objects.all()
    context['girl_size'] = Girl.objects.all()
    context['form'] = OrderForm(request.POST or None)
    return render(request, 'checkout.html', context)

class Make_order(View):
    
    def post(self,request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        cus = request.user
        c = user_cart(cus)
        cart = c
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = cart.customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.adress = form.cleaned_data['adress']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            cart.in_order = True
            cart.save()
            new_order.cart = cart
            new_order.save()
            cart.customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Ваше замовлення прийнято, дякуємо та бажаємо гарного дня!')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')