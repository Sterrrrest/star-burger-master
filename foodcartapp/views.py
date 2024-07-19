from django.http import JsonResponse
from django.templatetags.static import static
import json
import re
import requests

from foodcartapp.models import Product
from foodcartapp.models import Order, OrderDetail

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.serializers import CharField, ListField, IntegerField, DictField, ModelSerializer

from errors import get_null, get_space




@api_view(['GET'])
def banners_list_api(request):
    # FIXME move data to db?
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
    products = ListField(child=OrderDetailSerializer(), allow_empty=False)

    def validate_phonenumber(self, value):
        phone_format = re.compile('^\+?[78][1-9][-\(]?\d{2}\)?-?\d{3}-?\d{2}-?\d{2}$')

        if not phone_format.search(value):
            raise ValidationError('Hеверный формат номера телефона')
        return value

    class Meta:
        model = Order
        fields = ['products', 'phonenumber', 'firstname', 'lastname', 'address']

@api_view(['POST'])
def register_order(request):
    try:
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        products = request.data.get('products')
        if not isinstance(products, list):
            raise ValidationError('Expects products field be a list')

        for fields in products:
            serializer = OrderDetailSerializer(data=fields)
            serializer.is_valid(raise_exception=True)

        order = Order.objects.create(firstname=serializer.validated_data['firstname'],
                                     lastname=serializer.validated_data['lastname'],
                                     phonenumber=serializer.validated_data['phonenumber'],
                                     address=serializer.validated_data['address'])

        for product in serializer.validated_data.get('products'):
            OrderDetail.objects.create(product=Product.objects.get(id=product.get('product')),
                                       quantity=product.get('quantity'),
                                       order=order)

    except ValueError:
        return Response({})

    except requests.exceptions.HTTPError:
        print('HTTPError')
    except requests.exceptions.ConnectionError:
        print('ConnectionError')

    return Response({})
