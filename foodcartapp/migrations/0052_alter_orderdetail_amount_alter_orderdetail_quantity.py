# Generated by Django 5.0.7 on 2024-08-14 13:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0051_alter_order_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Стоимость'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='quantity',
            field=models.IntegerField(max_length=2, verbose_name='Количество'),
        ),
    ]
