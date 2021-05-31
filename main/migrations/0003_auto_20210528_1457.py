# Generated by Django 3.2 on 2021-05-28 12:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210527_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=datetime.datetime(2021, 5, 28, 12, 57, 17, 140472, tzinfo=utc), verbose_name='Бажана дата отримання замовлення'),
        ),
        migrations.AlterField(
            model_name='order',
            name='buying_type',
            field=models.CharField(choices=[('delivery', 'Доставка'), ('self', 'Самовивіз')], default='self', max_length=225, verbose_name='Тип замовлення'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('is_ready', 'Замовлення готове'), ('completed', 'Замовлення виконане'), ('in_progress', 'Замовлення обробляється'), ('new', 'Нове зомовлення')], default='new', max_length=225, verbose_name='Статус замовлення'),
        ),
    ]