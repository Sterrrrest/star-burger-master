# Generated by Django 5.0.7 on 2024-08-05 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interval', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geoplace',
            name='address',
            field=models.TextField(max_length=200, unique=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='geoplace',
            name='lat',
            field=models.CharField(max_length=200, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='geoplace',
            name='lon',
            field=models.CharField(max_length=200, verbose_name='Долгота'),
        ),
    ]
