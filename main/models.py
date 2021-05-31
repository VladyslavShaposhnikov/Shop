from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
import datetime

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
    pub_date = models.DateTimeField(verbose_name='Дата публікації')

    def new_product(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days=30))
    
    def __str__(self):
        return self.title

class Cart(models.Model):
    customer = models.ForeignKey('Customer', null=True, verbose_name='Власник кошика', on_delete=models.CASCADE)
    product_in_cart = models.ManyToManyField('CartProduct', blank=True, verbose_name='Продукти в корзині')
    final_price = models.DecimalField(default=0, decimal_places=2, max_digits=9, verbose_name='Кінцева сумма')
    final_count_of_items = models.PositiveIntegerField(verbose_name='Кількість всіх продуктів у корзині', default=0)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return 'Корзина покупця: {} '.format(self.id)

def recalculate_cart(cart):
    cart_data = cart.product_in_cart.aggregate(models.Sum('final_price'), models.Sum('qty'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data.get('final_price__sum')
        cart.final_count_of_items = cart_data.get('qty__sum')
    else:
        cart.final_price = 0
        cart.final_count_of_items = 0
    cart.save()

class CartProduct(models.Model):
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE)
    basket = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(default=0, decimal_places=2, max_digits=9, verbose_name='Кінцева сумма')

    def __str__(self):
        return 'Продукт кошика: {}'.format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args,**kwargs)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=75,verbose_name='Номер телефону', null=True, blank=True)
    adress = models.CharField(max_length=75,verbose_name='Домашній адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Замовлення покупця', related_name='related_customer')

    def __str__(self):
        return 'Клієнт: {} {}'.format(self.user.first_name, self.user.last_name)

class Boy(Product):
    sizon = models.CharField(max_length=125, verbose_name='Сезон')
    size = models.CharField(verbose_name='Розмір', max_length=75)
    age = models.CharField(max_length=75, verbose_name='Вік')
    brand = models.CharField(max_length=75, verbose_name='Бренд',null=True,blank=True)
    material = models.CharField(max_length=75, verbose_name='Состав',null=True,blank=True)
    father = models.ForeignKey('self',related_name='variants', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.father == None:
            return '__{}__'.format(self.title)
        else:
            return '{}({})'.format(self.title, self.size)

    def get_absolute_url(self):
        get_product_url(self, 'pro_det')

class Girl(Product):
    sizon = models.CharField(max_length=125, verbose_name='Сезон')
    size = models.CharField(verbose_name='Розмір', max_length=75)
    age = models.CharField(max_length=75, verbose_name='Вік')
    brand = models.CharField(max_length=75, verbose_name='Бренд',null=True,blank=True)
    material = models.CharField(max_length=75, verbose_name='Состав',null=True,blank=True)
    father = models.ForeignKey('self',related_name='variants', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.father == None:
            return '__{}__'.format(self.title)
        else:
            return '{}({})'.format(self.title, self.size)

    def get_absolute_url(self):
        get_product_url(self, 'pro_det')

class Baby(Product):
    sizon = models.CharField(max_length=125, verbose_name='Сезон')
    size = models.CharField(verbose_name='Розмір', max_length=75)
    age = models.CharField(max_length=75, verbose_name='Вік')
    brand = models.CharField(max_length=75, verbose_name='Бренд',null=True,blank=True)
    material = models.CharField(max_length=75, verbose_name='Состав',null=True,blank=True)
    father = models.ForeignKey('self',related_name='variants', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.father == None:
            return '__{}__'.format(self.title)
        else:
            return '{}({})'.format(self.title, self.size)

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

class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOISES = {
        (STATUS_NEW, 'Нове зомовлення'),
        (STATUS_IN_PROGRESS, 'Замовлення обробляється'),
        (STATUS_READY, 'Замовлення готове'),
        (STATUS_COMPLETED, 'Замовлення виконане')
    }

    BUYING_TYPE_CHOISES = {
        (BUYING_TYPE_SELF, 'Самовивіз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    }

    customer = models.ForeignKey('Customer', verbose_name='Замовник', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=75, verbose_name="Ім'я")
    last_name = models.CharField(max_length=75, verbose_name='Прізвище')
    phone = models.CharField(max_length=75, verbose_name='Телефон')
    adress = models.CharField(max_length=550, verbose_name='Адрес доставки', null=True, blank=True)
    status = models.CharField(
        max_length = 225,
        verbose_name = 'Статус замовлення',
        choices = STATUS_CHOISES,
        default = STATUS_NEW
    )
    buying_type = models.CharField(
        max_length = 225,
        verbose_name = 'Тип замовлення',
        choices = BUYING_TYPE_CHOISES,
        default = BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Коментарій до замовлення', null=True, blank=True)
    created_data = models.DateTimeField(auto_now=True, verbose_name='Дата створення замовлення')
    order_date = models.DateField(default=timezone.now(), verbose_name='Бажана дата отримання замовлення')
    cart = models.ForeignKey(Cart, verbose_name='Кошик', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.last_name, self.id)