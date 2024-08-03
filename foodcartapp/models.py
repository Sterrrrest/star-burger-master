from django.db import models
from django.db.models import F
from django.db.models import Count, Sum

from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.core.files.base import ContentFile
from django.utils import timezone



class OrderQuerySet(models.QuerySet):

    def price(self):

        sum = self.annotate(sum=Sum(F('order_details__quantity') * F('order_details__product__price'))).order_by('id')

        return sum


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class Order(models.Model):
    firstname = models.CharField(verbose_name="Имя заказчика", max_length=200, db_index=True)
    lastname = models.CharField(verbose_name="Фамилия заказчика", max_length=200, db_index=True)
    phonenumber = PhoneNumberField(region='RU', verbose_name="Номер телефон")
    address = models.TextField(verbose_name="Адрес", max_length=200, db_index=True, blank=True)
    restaurant = models.ForeignKey('Restaurant', related_name='orders', on_delete=models.CASCADE, null=True)
    registered_at = models.DateTimeField(verbose_name='Время создания заказа', default=timezone.now, db_index=True)
    called_at = models.DateTimeField(verbose_name='Время звонка', null=True, db_index=True, blank=True)
    delivered_at = models.DateTimeField(verbose_name='Время доставки', null=True, db_index=True, blank=True)

    class Status(models.TextChoices):
        ACC = '1', 'Принят'
        PRE = '2', 'Готовиться'
        DEL = '3', 'Доставляется'
        FIN = '4', 'Доставлен'

    class Payment(models.TextChoices):
        CAS = '1', 'Наличные'
        ONL = '2', 'Онлайн'
        CAR = '3', 'Картой'

    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ACC, db_index=True)
    payment = models.CharField(max_length=2, choices=Payment.choices, default=Payment.CAS, db_index=True)

    comment = models.TextField(verbose_name='Комментарий', max_length=400, blank=True)

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class OrderDetail(models.Model):
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField(verbose_name='Количество')
    order = models.ForeignKey(Order, verbose_name='Клиент', on_delete=models.CASCADE, related_name='order_details')
    amount = models.DecimalField(verbose_name="Стоимость", max_digits=8, decimal_places=2,
                                 validators=[MinValueValidator(0)], default=0.00)
    class Meta:
        verbose_name = 'Детали заказа'

    def __str__(self):
        return f'{self.product.name} {self.order.firstname} {self.order.lastname}'


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"
