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

def index(request):
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
        return context

class Categorydetail(DetailView):
    
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

    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['boys'] = boys
        context['girls'] = girls
        context['baby'] = baby
        context['toys'] = toys
        context['sport'] = sport
        return context

Boys = ('shoes','blouse', 'jacket', 'underwear', 'socks', 'reglan', 'sportswear', 't-short', 'hat', 'pants')
Girls = ('shoes-for-girl','blouse-for-girl', 'jacket-for-girl', 'dress', 'underwear-for-girl', 'reglan-for-girl', 'sportswear-for-girl', 't-short-for-girl', 'hat-for-girl', 'pants-for-girl', 'tights-for-girl')
Toy = ('for-girls', 'for-boys', 'constructors', 'stuffed-animals', 'musical-toys', 'board-games', 'educational-toys')
Spor = ('cycling', 'skateboards', 'sled', 'scooters')
def categorydetail(request,slug):
    context['category'] = Category.objects.get(slug=slug)
    if slug in Boys:
        model = Boy
    elif slug in Girls:
        model = Girl
    elif slug in Toy:
        model = Toys
    elif slug in Spor:
        model = Sport
    else:
        model = Baby
    context['cats'] = model.objects.filter(category__slug=slug)
    return render(request, 'category_detail.html', context)