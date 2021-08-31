from django.db.models import Prefetch
from django_filters.rest_framework import backends
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from addresses.models import Address
from branches.models import BranchItem
from mixins.paginator import CustomPagination
from products.api.serializers import ProductSerializer, ProductBranchItemSerializer, ProductCreationSerializer, \
    CategorySerializer
from products.models import Item, Category


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (backends.DjangoFilterBackend, SearchFilter)
    filter_fields = ['is_available', 'created_at', 'categories__title']
    search_fields = ['title', 'categories__title']
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        """
        list api to retrieve items based on user location and minimum price
        """
        user_id = request.user.id
        address_id = request.query_params["address"]
        user_city = Address.objects.filter(id=address_id, user_id=user_id).values_list('city_id', flat=True)
        if user_city:
            city_id = user_city[0]
        else:
            return Response({"message": "no branches  found for this address", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        items_queryset = Item.objects.filter(branchitem__branch__cities__id=city_id,
                                             is_available=True) \
            .prefetch_related(
            Prefetch('branchitem_set',
                     queryset=BranchItem.objects.filter(branch__cities__id=city_id)))
        items_queryset = items_queryset.distinct('id')

        if items_queryset:
            queryset = self.paginate_queryset(self.filter_queryset(items_queryset))
            serializer = ProductBranchItemSerializer(queryset, many=True)
            return self.paginator.get_paginated_response(serializer.data)
        else:
            serializer = ProductBranchItemSerializer(items_queryset, many=True)
            return Response({"result": serializer.data, "message": "Done", "status": True},
                            status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        """
        create item in database
        """
        data = request.data
        serializer = ProductCreationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data, "message": "Done", "status": True},
                            status=status.HTTP_201_CREATED)
        return Response({"message": serializer.errors, "status": False}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        retrieve item by id and if its available
        """
        item_id = kwargs["pk"]
        user_id = request.user.id
        address_id = request.query_params["address"]
        user_city = Address.objects.filter(id=address_id, user_id=user_id).values_list('city_id', flat=True)
        if user_city:
            city_id = user_city[0]
        else:
            return Response({"message": "no branches  found for this address", "status": False}, status=status.HTTP_400_BAD_REQUEST)

        item_queryset = Item.objects.filter(id=item_id, branchitem__branch__cities__id=city_id,
                                            is_available=True) \
            .prefetch_related(
            Prefetch('branchitem_set',
                     queryset=BranchItem.objects.filter(item__id=item_id, branch__cities__id=city_id)))
        item_queryset = item_queryset.distinct("id")
        serializer = ProductSerializer(item_queryset, many=True)
        return Response({"result": serializer.data, "message": "Done", "status": True}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        update existing items
        """
        data = request.data
        product = get_object_or_404(Item, id=kwargs["pk"])
        serializer = ProductCreationSerializer(instance=product, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data, "message": "Done", "status": True}, status=status.HTTP_200_OK)
        return Response({"message": serializer.errors, "status": False}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        delete item
        """
        product = get_object_or_404(Item, id=kwargs["pk"])
        product.delete()
        return Response({"message": "Done", "status": True}, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        address_id = request.query_params["address"]
        user_city = Address.objects.filter(id=address_id, user_id=user_id).values_list('city_id', flat=True)
        if user_city:
            city_id = user_city[0]
        else:
            return Response({"message": "no branches  found for this address", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        category_queryset = Category.objects.filter(item__branchitem__branch__cities__id=city_id) \
            .prefetch_related(
            Prefetch('item_set',
                     queryset=Item.objects.filter(branchitem__branch__cities__id=city_id).distinct(
                         'id'),
                     to_attr='category_items'))

        category_queryset = category_queryset.distinct('id')
        serializer = CategorySerializer(category_queryset, many=True)
        return Response({"result": serializer.data, "message": "Done", "status": True}, status=status.HTTP_200_OK)
