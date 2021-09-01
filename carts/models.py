from decimal import Decimal
from django.db import models
from django.db.models import Sum, F
from helpers.models import Timestamps


class Cart(Timestamps):
    """
    store cart details (order_id - address_id)
    """
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey("addresses.Address", on_delete=models.CASCADE, default=4)

    def __str__(self):
        return str(self.id)

    @property
    def cart_total(self):
        # calculated field to calculate total price of all cart items
        return self.cart_item.aggregate(
            total_price=Sum(F('quantity') * F('price'))
        )["total_price"] or Decimal(0)

    @property
    def shipping_fee(self):
        # calculated field to calculate shipping fees depending on total price if its > 100 shipping is 0 else shipping is 20
        if self.cart_total > 100:
            return Decimal(0)
        return Decimal(20)

    @property
    def grand_total(self):
        # calculated field to calculate grand total cart_total + shipping_fee
        return Decimal(self.cart_total + self.shipping_fee)


class CartItem(Timestamps):
    """
    store CartItem data (cart_id - item_id - quantity - price)
    """
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE, related_name='cart_item')
    item = models.ForeignKey('products.Item', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    @property
    def item_total(self):
        # calculated field to calculate item total_price = quantity * price
        return Decimal(self.price * self.quantity)

    def __str__(self):
        return str(self.cart)

