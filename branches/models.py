from decimal import Decimal

from django.db import models
from django.db.models import F, Min

from helpers.models import Timestamps


class City(Timestamps):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"


class Branch(Timestamps):
    name = models.CharField(max_length=255)
    cities = models.ManyToManyField('City')

    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name


class BranchItem(Timestamps):
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    item = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    @property
    def price(self):

        x = BranchItem.objects.all().aggregate(Min(F('item__price')))
        print(x)
        # return self.item.aggregate(
        #     price=Min(F('item__price'))
        # )["price"]
        return Decimal(1)
