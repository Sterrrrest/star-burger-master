from rest_framework.serializers import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.serializers import CharField, ListField, IntegerField, DictField, ModelSerializer

from foodcartapp.models import Order, OrderDetail, Product


class OrderDetailSerializer(ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderDetailSerializer(many=True, allow_empty=False, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'phonenumber', 'firstname', 'lastname', 'address', 'products']
