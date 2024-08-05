import requests

from django.shortcuts import render

from .models import GeoPlace

from environs import Env

env = Env()
env.read_env()


def fetch_coordinates(address):
    if GeoPlace.objects.filter(address=address).exists():

        lon = GeoPlace.objects.get(address=address).lon
        lat = GeoPlace.objects.get(address=address).lat

        return lon, lat

    else:
        apikey = env.str('YANDEX_API_KEY')

        base_url = "https://geocode-maps.yandex.ru/1.x"
        response = requests.get(base_url, params={
            "geocode": address,
            "apikey": apikey,
            "format": "json",
        })
        response.raise_for_status()
        found_places = response.json()['response']['GeoObjectCollection']['featureMember']

        if not found_places:
            return None

        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")

        geo = GeoPlace.objects.create(address=address,
                                lon=lon,
                                lat=lat)

        lon = geo.lon
        lat = geo.lat

        return lon, lat
