from rest_framework import serializers
from branches.models import BranchItem
from carts.models import Cart, CartItem
from addresses.models import Address
from utils.utils import calculate_price


class CartItemSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    name = serializers.CharField(source='item.title')
    # image = serializers.SerializerMethodField()
    description = serializers.CharField(source='item.description')
    item_total = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_image(self, CartItem):
        # return item image full path
        request = self.context.get('request')
        photo_url = CartItem.item.image.url
        return request.build_absolute_uri(photo_url)

    def get_item_total(self, instance):
        # return a specific format "10 SAR"
        return "{} SAR".format(instance.item_total)

    def get_price(self, instance):
        # return a specific format "10 SAR"
        return "{} SAR".format(instance.price)

    def to_internal_value(self, data):
        # add extra data to {data dict}
        data['cart'] = self.context.get('cart')
        data['address_id'] = self.context.get('address_id')
        data['user_id'] = self.context.get('user_id')
        return data

    class Meta:
        model = CartItem
        fields = "__all__"

    def create(self, validated_data):
        """
        this function is used to add item to a cart if the item doesn't exist in user cart if it does exist then
        the item quantity will be updated
        """
        cart = validated_data.get('cart')
        item_id = validated_data.get('item_id')
        user_id = validated_data.get('user_id')
        updated_quantity = validated_data.get('quantity')
        address_id = validated_data.get('address_id')
        # get user city_id to search for branch items in this city
        user_city = Address.objects.get(id=address_id, user_id=user_id)
        city_id = user_city.city_id
        # search for branch items
        branch_items = BranchItem.objects.filter(item_id=item_id, branch__city_id=city_id, is_available=True)
        # send branch items to calculate_price function to get the best price (min)
        best_price = calculate_price(branch_items)
        # check if the item already added to the cart before it it does then its quantity will be updated
        cart_item_exist = CartItem.objects.filter(cart_id=cart.id, item_id=item_id).exists()
        if cart_item_exist:
            cart_item = CartItem.objects.get(cart_id=cart.id, item_id=item_id)
            cart_item.quantity = updated_quantity
            cart_item.save()

        else:
            # else a new cart item will be created to be added to the user cart
            cart_item = CartItem.objects.create(cart_id=cart.id, item_id=item_id, quantity=updated_quantity,
                                                price=best_price)
        return cart_item


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cart_item', many=True)
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    cart_total = serializers.SerializerMethodField()
    shipping_fee = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()

    def get_cart_total(self, instance):
        # return a specific format "10 SAR"
        return "{} SAR".format(instance.cart_total)

    def get_shipping_fee(self, instance):
        # return a specific format "10 SAR"
        return "{} SAR".format(instance.shipping_fee)

    def get_grand_total(self, instance):
        # return a specific format "10 SAR"
        return "{} SAR".format(instance.grand_total)

    class Meta:
        model = Cart
        fields = "__all__"

    def to_representation(self, instance):
        # return address data with the response
        data = super().to_representation(instance)
        print(instance)
        address = instance.address
        address_data = Address.objects.filter(id=address.id).values('title', 'city__name', 'address_info')
        data["address"] = {"title": address_data[0]['title'], "city": address_data[0]['city__name'],
                           'details': address_data[0]['address_info']}
        return data
