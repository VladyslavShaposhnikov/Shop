from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('categories/', show_categories, name='categories'),
    path('product/<str:ct_model>/<slug:slug>/', Productdetail.as_view(), name='pro_det'),
    path('category/<slug:slug>/', categorydetail, name='cat_det'),
]