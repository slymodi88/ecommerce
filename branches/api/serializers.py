# from rest_framework import serializers
#
# from branches.models import BranchItem
# from products.api.serializers import ProductSerializer
#
#
# class BranchItemSerializer(serializers.ModelSerializer):
#     item = ProductSerializer()
#     price = serializers.SerializerMethodField()
#
#     class Meta:
#         model = BranchItem
#         fields = "__all__"
#
#     def get_price(self, instance):
#         return "{} SAR".format(instance.price)
#
#     # def get_price(self, instance):
#     #     return "{} SAR".format(instance.price)
