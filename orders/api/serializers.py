from rest_framework import serializers
from carts.models import Cart, CartItem
from addresses.models import Address
from orders.models import OrderProduct, Order
from django.shortcuts import get_object_or_404

from utils.utils import send_order_email


class OrderCreateSerializer(serializers.ModelSerializer):
    order_total = serializers.SerializerMethodField()
    shipping_fee = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()

    def get_order_total(self, instance):
        # return a specific format "10 SAR"
        return "{} SAR".format(instance.order_total)

    def get_shipping_fee(self, instance):
        # return a specific format "10 SAR"
        return "{} SAR".format(instance.shipping_fee)

    def get_grand_total(self, instance):
        # return a specific format "10 SAR"
        return "{} SAR".format(instance.grand_total)

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        """
        create user order  then lock the user's cart related to this order
        """
        user = validated_data.get('user')
        email = user.email
        cart = get_object_or_404(Cart, address__user=user, order=None)
        order = Order.objects.create(user=user, order_total=cart.cart_total, grand_total=cart.grand_total,
                                     shipping_fee=cart.shipping_fee)
        cart.order = order
        cart.save()
        # get cart_items related to user cart and create order_product for each item
        items = CartItem.objects.filter(cart=cart)
        for item in items:

            OrderProduct.objects.create(order=order, item=item.item, quantity=item.quantity, price=item.item.price)
        order.save()
        # send email to user after order creation
        send_order_email(email)
        return order

    def to_representation(self, instance):
        # return address data with the response
        data = super().to_representation(instance)
        user = instance.user
        data["address"] = Address.objects.filter(user=user).values('title', 'city', 'address_info')
        return data


class OrderSerializer(serializers.ModelSerializer):
    order_total = serializers.SerializerMethodField()
    shipping_fee = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()

    def get_order_total(self, instance):
        # return a specific format "10 SAR"
        return "{} SAR".format(instance.order_total)

    def get_shipping_fee(self, instance):
        # return a specific format "10 SAR"
        return "{} SAR".format(instance.shipping_fee)

    def get_grand_total(self, instance):
        # return a specific format "10 SAR"
        return "{} SAR".format(instance.grand_total)

    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        # return address data with the response
        data = super().to_representation(instance)
        user = instance.user
        data["address"] = Address.objects.filter(user=user).values('title', 'city', 'address_info')
        return data
