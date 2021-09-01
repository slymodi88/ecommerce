from django.contrib.gis.db import models
from django.utils import timezone

from helpers.models import Timestamps


class Order(Timestamps):
    """
    order model to hold user order data such as total and delivery date
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_order', default=1)
    order_total = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    grand_total = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True, default=timezone.now().date())
    shipping_fee = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    address = models.ForeignKey("addresses.Address", on_delete=models.CASCADE, default=4)

    def __str__(self):
        return str(self.id)


class OrderProduct(Timestamps):
    """
    store order_product data (order_id - item_id - quantity - price)
    """
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('products.Item', on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return str(self.id)
