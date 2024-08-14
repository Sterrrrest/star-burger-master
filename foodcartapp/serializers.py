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

    def create(self, validated_data):

        order = Order.objects.create(firstname=validated_data['firstname'],
                                     lastname=validated_data['lastname'],
                                     phonenumber=validated_data['phonenumber'],
                                     address=validated_data['address'])

        for product in validated_data['products']:
           order_detail = OrderDetail.objects.create(product=Product.objects.get(id=product['product'].id),
                                       quantity=product['quantity'],
                                       order=order)

        return order

    class Meta:
        model = Order
        fields = ['id', 'phonenumber', 'firstname', 'lastname', 'address', 'products']
