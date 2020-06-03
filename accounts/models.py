from django.db import models

CATEGORIES = (
    ('EARPHONE', 'earphone'),
    ('HEADPHONE', 'headphone'),
    ('LAPTOP', 'laptop'),
)


class AddProductModel(models.Model):
    product_name = models.CharField(max_length=20, choices=CATEGORIES)
    product_description = models.CharField(max_length=100)
    product_price = models.IntegerField()
    product_quantity = models.IntegerField(default=0)


PRODUCT_QUANTITY = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
)


class PlaceOrderModel(models.Model):
    order_by = models.CharField(max_length=20, null=True)
    product_name = models.CharField(max_length=50, null=True)
    product_quantity = models.IntegerField(choices=PRODUCT_QUANTITY, default=1)
    product_price = models.IntegerField(null=True)
    product_status = models.CharField(max_length=10, null=True)
