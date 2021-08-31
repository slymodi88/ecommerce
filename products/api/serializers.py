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
        return "{} SAR".format(instance.calculate_price(instance.branchitem_set.all()))

    def get_is_available(self, instance):
        return instance.get_is_available(instance.branchitem_set.all())

    def get_branch(self, instance):
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
        return "{} SAR".format(instance.calculate_price(instance.branchitem_set.all()))

    def get_is_available(self, instance):
        return instance.get_is_available(instance.branchitem_set.all())

    def get_branch(self, instance):
        branch_items = instance.branchitem_set.filter(is_available=True).order_by('price')
        if branch_items:
            return branch_items.values('branch_id', 'branch__name')[0]
        return None


class CategoryItemsSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ('id', 'title', 'price', 'is_available', 'image')

    def get_price(self, instance):
        return "{} SAR".format(instance.calculate_price(instance.branchitem_set.all()))

    def get_is_available(self, instance):
        return instance.get_is_available(instance.branchitem_set.all())


class CategorySerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    def get_items(self, instance):
        return CategoryItemsSerializer(instance.get_category_items(), many=True).data
