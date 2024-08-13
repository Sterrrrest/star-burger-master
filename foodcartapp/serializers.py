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

    def validate_phonenumber(self, value):
        phone_format = re.compile('^\+?[78][1-9][-\(]?\d{2}\)?-?\d{3}-?\d{2}-?\d{2}$')

        if not phone_format.search(value):
            raise ValidationError('Hеверный формат номера телефона')
        return value

    class Meta:
        model = Order
        fields = ['id', 'phonenumber', 'firstname', 'lastname', 'address', 'products']
