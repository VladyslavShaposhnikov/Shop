from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin

admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(BoyGirlBaby)