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
        address_id = request.query_params["address_id"]
        category_id = request.query_params["category_id"]
        try:
            # check if the entered address is correct if not raise exception
            user_address = Address.objects.get(id=address_id, user_id=user_id)
        except:
            return Response({"message": "Wrong Address", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        city_id = user_address.city_id
        # return all available items that its branch items is in user city and have a specific category
        items_queryset = Item.objects.filter(branchitem__branch__city_id=city_id,
                                             is_available=True, categories__id=category_id) \
            .prefetch_related(
            Prefetch('branchitem_set',
                     queryset=BranchItem.objects.filter(branch__city_id=city_id)))
        # remove duplicated items
        items_queryset = items_queryset.distinct('id')

        # checks it the returned items_queryset is empty or not if empty send it serializer directly to avoid paginator errors else send to paginator first
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
        address_id = request.query_params["address_id"]
        # check if the entered address is correct if not raise exception
        try:
            user_address = Address.objects.get(id=address_id, user_id=user_id)
        except:
            return Response({"message": "Wrong Address", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        city_id = user_address.city_id
        # return a specific available item with its branch items in user city
        item_queryset = Item.objects.filter(id=item_id, branchitem__branch__city_id=city_id,
                                            is_available=True) \
            .prefetch_related(
            Prefetch('branchitem_set',
                     queryset=BranchItem.objects.filter(item__id=item_id, branch__city_id=city_id)))
        # remove duplicated items
        item_queryset = item_queryset.distinct("id")
        serializer = ProductSerializer(item_queryset, many=True)
        return Response({"result": serializer.data, "message": "Done", "status": True}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        update existing items
        """
        data = request.data
        # get a specific item or return error if it's not found
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
        # get a specific item or return error if it's not found
        product = get_object_or_404(Item, id=kwargs["pk"])
        product.delete()
        return Response({"message": "Done", "status": True}, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        address_id = request.query_params["address_id"]
        try:
            user_address = Address.objects.get(id=address_id, user_id=user_id)
        except:
            return Response({"message": "Wrong Address ", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        city_id = user_address.city_id
        # get all categories that have branch items in user city "distinct is to remove duplicated results "
        category_queryset = Category.objects.filter(item__branchitem__branch__city_id=city_id).distinct("id")
        serializer = CategorySerializer(category_queryset, many=True)
        return Response({"result": serializer.data, "message": "Done", "status": True}, status=status.HTTP_200_OK)
