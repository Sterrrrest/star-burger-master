from django.db import models

class GeoPlace(models.Model):
    address = models.TextField(verbose_name="Адрес", max_length=200, unique=True)
    lat = models.CharField(verbose_name="Широта", max_length=200)
    lon = models.CharField(verbose_name="Долгота", max_length=200)

