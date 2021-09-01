from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from carts.api.serializers import CartSerializer, CartItemSerializer
from carts.models import Cart, CartItem


class CartApi(GenericViewSet):
    permission_classes = (IsAuthenticated,)

    @action(methods=['get'], detail=False)
    def details(self, request, *args, **kwargs):
        user_id = request.user.id
        # search for an existing cart for this user that hasn't been attached to an order yet if there is no cart a new cart will be created
        cart, created = Cart.objects.get_or_create(address__user_id=user_id, order=None)
        serializer = CartSerializer(cart)
        return Response({"result": serializer.data, "message": "Done", "status": True},
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def add_product(self, request):
        user_id = request.user.id
        data = request.data
        address_id = request.query_params["address_id"]
        # search for an existing cart for this user that hasn't been attached to an order yet if there is no cart a new cart will be created
        cart, created = Cart.objects.get_or_create(address__user_id=user_id, order=None)
        serializer = CartItemSerializer(data=data, context={'cart': cart, 'address_id': address_id, 'user_id': user_id,
                                                            'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data, "message": "Done", "status": True},
                            status=status.HTTP_200_OK)
        return Response({"result": serializer.errors, "message": "Done", "status": False},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=False)
    def remove_item(self, request):
        user_id = request.user.id
        data = request.data
        # get user cart so an item can be removed form it
        cart = Cart.objects.get(address__user_id=user_id, order=None)
        item = CartItem.objects.filter(cart=cart, item_id=data['item_id'])
        item.delete()
        return Response({"message": "Done", "status": True}, status=status.HTTP_200_OK)
