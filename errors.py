
from rest_framework.response import Response

# def get_isinstance(request_order):
#     return Response(f'{field}: Ожидался str со значениями, но был получен "list" или пустой')


# def get_obligatory_field(error):
#     for field in request_order:
def get_null(request_order):
    null = []
    null_fields = ''

    for field in request_order:
        if request_order.get(field) is None:
            null.append(field)
    for empty_field in null:
        null_fields += str(empty_field)
        null_fields += ' '
    return Response(f'Это поле: {null_fields}не может быть пустым.')

def get_space(request_order):
    empty = []
    empty_fields = ''
    for field in request_order:
        if not request_order.get(field):
            empty.append(field)
    for empty_field in empty:
        empty_fields += str(empty_field)
        empty_fields += ' '
    return Response(f'Это поле: {empty_fields}не может быть пустым.')


# request_order = {"products": [{"product": 1, "quantity": 1}], "firstname": '', "lastname": '', "phonenumber": '', "address": 'null'}
# print(request_order['products'][0])
# empty = []
# empty_fields = ''
# for field in request_order:
#     if request_order.get(field) == '':
#         empty.append(field)
# for empty_field in empty:
#     empty_fields += str(empty_field)
#     empty_fields += ' '
# print(empty)
