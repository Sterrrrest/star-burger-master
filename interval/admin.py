from django.contrib import admin

from interval.models import GeoPlace


@admin.register(GeoPlace)
class GeoPlaceAdmin(admin.ModelAdmin):
    pass
# Register your models here.
