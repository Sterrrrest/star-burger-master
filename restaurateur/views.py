import requests

from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.db.models import F

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

from geopy import distance

from foodcartapp.models import Order, OrderDetail
from foodcartapp.models import Product, Restaurant, RestaurantMenuItem
from interval.models import GeoPlace

from interval.views import fetch_coordinates


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    try:
        orders = Order.objects.price().exclude(status=4).prefetch_related('order_details').order_by('status')
        available_restaurants = []

        for order in orders:

            first_product_restaurants = []
            product_restaurants = []

            restaurant_first_product = RestaurantMenuItem.objects.filter(product_id=order.order_details.first().product.id)
            for rest in restaurant_first_product:
                first_product_restaurants.append(rest.restaurant)

            for r in first_product_restaurants:
                t = []
                products_in_rest = RestaurantMenuItem.objects.filter(restaurant=r)
                for product_in_od in order.order_details.all():
                    if products_in_rest.filter(product=product_in_od.product).exists():
                        if r not in t:
                            t.append(r)
                    else:
                        t.clear()
                        break
                if t:
                    product_restaurants.append(t[0])
            order_coords = fetch_coordinates(order.address)
            restar =[]
            for ar in product_restaurants:

                rest_coords = fetch_coordinates(ar.address)
                restaurants = {'restaurant': ar,
                               'interval': distance.distance(rest_coords, order_coords).km
                               }
                restar.append(restaurants)

            available_restaurant = {'order': order, 'restaurants': sorted(restar, key=lambda d: d['interval'])}
            available_restaurants.append(available_restaurant)

    except requests.RequestException as e:
        print('Ошибка запроса', e)
    except requests.ConnectionError as e:
        print('Ошибка подключения', e)

    return render(request, template_name='order_items.html', context={'available_restaurants': available_restaurants})
