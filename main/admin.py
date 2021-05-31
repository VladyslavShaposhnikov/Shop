from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *

admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Boy)
admin.site.register(Girl)
admin.site.register(Baby)
admin.site.register(Toys)
admin.site.register(Sport)
admin.site.register(Order)