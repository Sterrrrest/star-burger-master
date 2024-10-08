# Generated by Django 5.0.7 on 2024-08-02 12:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_auto_20240723_1942'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'заказ', 'verbose_name_plural': 'заказы'},
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('1', 'Принят'), ('2', 'Готовиться'), ('3', 'Доставляется'), ('4', 'Доставлен')], default='1', max_length=2),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Стоимость'),
        ),
    ]
