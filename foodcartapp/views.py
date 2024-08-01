import json
import re
import requests

from django.http import JsonResponse
from django.templatetags.static import static
from django.db import transaction

from foodcartapp.models import Order, OrderDetail, Product

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.serializers import CharField, ListField, IntegerField, DictField, ModelSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser




@api_view(['GET'])
def banners_list_api(request):
    return Response([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ])


@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return Response(dumped_products)


class OrderDetailSerializer(ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderDetailSerializer(many=True, allow_empty=False, write_only=True)

    def validate_phonenumber(self, value):
        phone_format = re.compile('^\+?[78][1-9][-\(]?\d{2}\)?-?\d{3}-?\d{2}-?\d{2}$')

        if not phone_format.search(value):
            raise ValidationError('Hеверный формат номера телефона')
        return value

    class Meta:
        model = Order
        fields = ['id', 'phonenumber', 'firstname', 'lastname', 'address', 'products']


@transaction.atomic
@api_view(['POST'])
def register_order(request):
    try:

        request_data = request.data
        serializer = OrderSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        order = Order.objects.create(firstname=serializer.validated_data['firstname'],
                                     lastname=serializer.validated_data['lastname'],
                                     phonenumber=serializer.validated_data['phonenumber'],
                                     address=serializer.validated_data['address'])

        for product in serializer.validated_data['products']:
            products = OrderDetail.objects.create(product=Product.objects.get(id=product['product'].id),
                                       quantity=product['quantity'],
                                       order=order)

    except ValueError:
        return Response({})

    except requests.exceptions.HTTPError:
        print('HTTPError')
    except requests.exceptions.ConnectionError:
        print('ConnectionError')

    return Response(OrderSerializer(order).data)
