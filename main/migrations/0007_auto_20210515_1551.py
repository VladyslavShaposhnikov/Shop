# Generated by Django 3.2 on 2021-05-15 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210512_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='final_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Кінцева сумма'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='product_in_cart',
            field=models.ManyToManyField(blank=True, to='main.CartProduct', verbose_name='Продукти в корзині'),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='final_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Кінцева сумма'),
        ),
    ]
