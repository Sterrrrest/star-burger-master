from django.http import JsonResponse
from django.templatetags.static import static
import json
import re

from foodcartapp.models import Product
from foodcartapp.models import Order, OrderDetail
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
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


# def register_order(request):
#     data = json.loads(request.body.decode())
#     print(data)

@api_view(['POST'])
def register_order(request):
    try:
        request_order = request.data

        last_product = Product.objects.all().last().id
        if request_order['products'][0]['product'] > last_product:
            return Response(f"Недопустимый первичный ключ {request_order['products'][0]['product']}")

        phone_format = re.compile('^\+?[78][1-9][-\(]?\d{2}\)?-?\d{3}-?\d{2}-?\d{2}$')

        if not phone_format.search(request_order['phonenumber']):
            return Response('неверный формат номера телефона')

        if not isinstance(request_order['products'], list):
            return Response('products: Ожидался list со значениями, но был получен "str" или пустой')

        for field in request_order:
            if not isinstance(request_order.get(field), str) and request_order.get(field) is not request_order['products']:
                return Response(f'{field}: Ожидался str со значениями, но был получен list')
            elif not request_order.get(field):
                return get_space(request_order)
            elif request_order.get(field) is None:
                return get_null(request_order)


        order = Order.objects.create(firstname=request_order['firstname'],
                             lastname=request_order['lastname'],
                             phone_number=request_order['phonenumber'],
                             address=request_order['address'])

        for product in request_order.get('products'):
            OrderDetail.objects.create(product=Product.objects.get(id=product.get('product')),
                                       quantity=product.get('quantity'),
                                       order=order)

        # print(data)
    except ValueError:
        return Response({})

    except KeyError as e:
        return Response(f'{e}: Обязательное поле')

    # except Exception:
    #     return get_null(request_order)

    return Response({})
