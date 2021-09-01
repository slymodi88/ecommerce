from django.db import models
from helpers.models import Timestamps


class City(Timestamps):
    """
    store city data
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"


class Branch(Timestamps):
    """
    store branch data (name-city)
    """
    name = models.CharField(max_length=255)
    city = models.ForeignKey('City', on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name


class BranchItem(Timestamps):
    """
    store branch_item data (branch-item-availability-price)
    """
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    item = models.ForeignKey('products.Item', on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=15)

    class Meta:
        # to prevent storing the same branch_item more than one time in database
        unique_together = ('item', 'branch')

    def __str__(self):
        return str(self.id)
