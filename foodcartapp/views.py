from django.http import JsonResponse
from django.templatetags.static import static
import json

from foodcartapp.models import Product
from foodcartapp.models import Order, OrderDetail
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


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

        if not isinstance(request_order['products'], list):
            return Response('products: Ожидался list со значениями, но был получен "str" или пустой')
        if request_order['products'] is None:
            return Response('products: Это поле не может быть пустым.')
        if not request_order['products']:
            return Response('products: Этот список не может быть пустым.')


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
        return Response(f'{e}: Этот список не может быть пустым.')

    return Response({})
