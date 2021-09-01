from rest_framework import serializers
from products.models import Item, Category


class ProductCreationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")

    class Meta:
        model = Item
        fields = "__all__"
        extra_kwargs = {"price": {"write_only": True}}


class ProductSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    price = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = "__all__"
        extra_kwargs = {"price": {"write_only": True}}

    def get_price(self, instance):
        # item will be sent to calculate_price function in Item model to return item best price
        return "{} SAR".format(instance.calculate_price(instance.branchitem_set.all()))

    def get_is_available(self, instance):
        # item will be sent to calculate_price function in Item model to return item availability
        return instance.get_is_available(instance.branchitem_set.all())

    def get_branch(self, instance):
        # return item branch details like id and name
        branch_items = instance.branchitem_set.filter(is_available=True)
        if branch_items:
            return branch_items.values('branch_id', 'branch__name')[0]
        return None


class ProductBranchItemSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    price = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = "__all__"
        extra_kwargs = {"price": {"write_only": True}}

    def get_price(self, instance):
        # item will be sent to calculate_price function in Item model to return item best price
        return "{} SAR".format(instance.calculate_price(instance.branchitem_set.all()))

    def get_is_available(self, instance):
        # item will be sent to calculate_price function in Item model to return item availability
        return instance.get_is_available(instance.branchitem_set.all())

    def get_branch(self, instance):
        # return item branch details like id and name
        branch_items = instance.branchitem_set.filter(is_available=True).order_by('price')
        if branch_items:
            return branch_items.values('branch_id', 'branch__name')[0]
        return None


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

