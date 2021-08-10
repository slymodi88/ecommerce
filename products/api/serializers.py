from rest_framework import serializers

from branches.models import BranchItem
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")

    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {"price": {"write_only": True}}


class ProductBranchItemSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {"price": {"write_only": True}}

    def get_price(self, instance):
        return "{} SAR".format(instance.product_branchitem[0].price)
