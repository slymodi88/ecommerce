# from rest_framework import status
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.viewsets import GenericViewSet
#
# from branches.api.serializers import BranchItemSerializer
# from branches.models import City, BranchItem
#
#
# class BranchApi(GenericViewSet):
#     permission_classes = (IsAuthenticated,)
#
#     @action(methods=['get'], detail=False)
#     def list_products(self, request, *args, **kwargs):
#         user = request.user.id
#         print(user)
#         city = City.objects.get(user=user)
#         queryset = BranchItem.objects.filter(branch__cities=city.id, item__isavailable=True)
#         print(queryset)
#         serializer = BranchItemSerializer(queryset, many=True)
#         return Response({"result": serializer.data, "message": "Done", "status": True},
#                         status=status.HTTP_200_OK)
