from django.urls import path
from .views import index, show_categories, productdetail, categorydetail

urlpatterns = [
    path('', index, name='index'),
    path('categories/', show_categories, name='categories'),
    path('product/<slug:slug>/', productdetail, name='pro_det'),
    path('category/<slug:slug>/', categorydetail, name='cat_det'),
]