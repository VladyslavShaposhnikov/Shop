from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model':ct_model, 'slug':obj.slug})

class Category(MPTTModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')


    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name='Назва товару')
    description = models.CharField(max_length=300, verbose_name='Опис товару')
    slug = models.SlugField(unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Ціна')
    photo = models.ImageField(verbose_name='Зображення')
    
    def __str__(self):
        return self.title

class Cart(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    product_in_cart = models.ManyToManyField('CartProduct', blank=True, verbose_name='Продукти в корзині')
    final_price = models.DecimalField(default=0, decimal_places=2, max_digits=9, verbose_name='Кінцева сумма')
    final_count_of_items = models.PositiveIntegerField(verbose_name='Кількість всіх продуктів у корзині', default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return 'Корзина покупця: {} {}'.format(self.customer.user.first_name, self.customer.user.last_name)

class CartProduct(models.Model):
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE)
    basket = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Кінцева сумма')

    def __str__(self):
        return 'Продукт кошика: {}'.format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args,**kwargs)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=75,verbose_name='Номер телефону')
    adress = models.CharField(max_length=75,verbose_name='Домашній адрес')

    def __str__(self):
        return 'Клієнт: {} {}'.format(self.user.first_name, self.user.last_name)

class Boy(Product):
    sizon = models.CharField(max_length=125, verbose_name='Сезон')
    size = models.TextField(verbose_name='Розмір')
    age = models.CharField(max_length=75, verbose_name='Вік')
    brand = models.CharField(max_length=75, verbose_name='Бренд',null=True,blank=True)
    material = models.CharField(max_length=75, verbose_name='Состав',null=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        get_product_url(self, 'pro_det')

class Girl(Product):
    sizon = models.CharField(max_length=125, verbose_name='Сезон')
    size = models.TextField(verbose_name='Розмір')
    age = models.CharField(max_length=75, verbose_name='Вік')
    brand = models.CharField(max_length=75, verbose_name='Бренд',null=True,blank=True)
    material = models.CharField(max_length=75, verbose_name='Состав',null=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        get_product_url(self, 'pro_det')

class Baby(Product):
    sizon = models.CharField(max_length=125, verbose_name='Сезон')
    size = models.TextField(verbose_name='Розмір')
    age = models.CharField(max_length=75, verbose_name='Вік')
    brand = models.CharField(max_length=75, verbose_name='Бренд',null=True,blank=True)
    material = models.CharField(max_length=75, verbose_name='Состав',null=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        get_product_url(self, 'pro_det')

class Toys(Product):
    age = models.CharField(max_length=75, verbose_name='Вік')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        get_product_url(self, 'pro_det')

class Sport(Product):
    age = models.CharField(max_length=75, verbose_name='Вік')
    brand = models.CharField(max_length=75, verbose_name='Бренд',null=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        get_product_url(self, 'pro_det')