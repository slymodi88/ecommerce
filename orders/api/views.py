from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from orders.api.serializers import OrderSerializer, OrderCreateSerializer
from orders.models import Order


class OrderApi(GenericViewSet):
    permission_classes = (IsAuthenticated,)

    @action(methods=['get'], detail=False)
    def details(self, request, *args, **kwargs):
        """
        list user orders
        """
        user_id = request.user.id
        order = Order.objects.filter(user_id=user_id)
        serializer = OrderSerializer(order, many=True)
        return Response({"result": serializer.data, "message": "Done", "status": True},
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def create_order(self, request):
        """
        create order
        """
        data = request.data
        data["user"] = request.user.id
        serializer = OrderCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": serializer.data, "status": True}, status=status.HTTP_200_OK)
        return Response({"result": serializer.errors, "message": "Done", "status": False},
                        status=status.HTTP_400_BAD_REQUEST)

