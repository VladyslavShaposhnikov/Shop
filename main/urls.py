from django.urls import path

from .views import index, show_categories

urlpatterns = [
    path('', index, name='index'),
    path('categories/', show_categories, name='categories'),
]