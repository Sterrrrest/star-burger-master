from django.http import JsonResponse
from django.templatetags.static import static
import json

from foodcartapp.models import Product
from foodcartapp.models import Order, OrderDetail
from rest_framework.decorators import api_view
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


@api_view(['POST'])
def register_order(request):
    try:
        data = request.body.decode()

        order = Order.objects.create(firstname=data['firstname'],
                             lastname=data['lastname'],
                             phone_number=data['phonenumber'],
                             address=data['address'])

        for product in data.get('products'):
            OrderDetail.objects.create(product=Product.objects.get(id=product.get('product')),
                                       quantity=product.get('quantity'),
                                       order=order)

        print(data)
    except ValueError:
        return Response({})
    # TODO это лишь заглушка
    return Response({})
