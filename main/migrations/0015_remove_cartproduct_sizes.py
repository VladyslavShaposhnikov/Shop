# Generated by Django 3.2 on 2021-05-19 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20210519_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartproduct',
            name='sizes',
        ),
    ]
