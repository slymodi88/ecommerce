from django.db import models
from helpers.models import Timestamps


class City(Timestamps):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"


class Branch(Timestamps):
    name = models.CharField(max_length=255)
    cities = models.ForeignKey('City', on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name


class BranchItem(Timestamps):
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    item = models.ForeignKey('products.Item', on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=15)

    class Meta:
        unique_together = ('item', 'branch')

    def __str__(self):
        return str(self.id)

    # @property
    # def price(self):
    #
    #     x = BranchItem.objects.all().aggregate(Min(F('item__price')))
    #     print(x)
    #     # return self.item.aggregate(
    #     #     price=Min(F('item__price'))
    #     # )["price"]
    #     return Decimal(1)
