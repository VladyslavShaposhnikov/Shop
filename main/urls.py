from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('categories/', show_categories, name='categories'),
    path('product/<slug:slug>/', boyproductdetail, name='boy_pro_det'),
    path('product/<slug:slug>/', girlproductdetail, name='girl_pro_det'),
    path('product/<slug:slug>/', babyproductdetail, name='baby_pro_det'),
    path('category/<slug:slug>/', categorydetail, name='cat_det'),
]