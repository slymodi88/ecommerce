from decimal import Decimal

from django.db import models

from helpers.models import Timestamps


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

    def get_category_items(self):
        """
        returns list of category items that exists in user's city
        :return: List items
        """
        items = self.category_items
        return items


class Item(Timestamps):
    """
    Product model is used to hold information about items such as price, its availability, title and image
    """
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    is_available = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    image = models.ImageField()
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField("Category")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']

    def calculate_price(self, branch_items):
        """
        calculate price according to available items if not return min price of items
        :param branch_items: branch_items is a queryset that each items in it must contains is_available attribute
        :return: Decimal price
        """
        available_prices = [branch_item.price for branch_item in branch_items if branch_item.is_available]
        if available_prices:
            return min(available_prices)
        return min([branch_item.price for branch_item in branch_items])

    def get_is_available(self, branch_items):
        """
        return if the item is available or not according to its package and branch availability
        :param branch_items: branch_items is a queryset that each items in it must contains is_available attribute
        :return: Boolean
        """
        available_items = [branch_item for branch_item in branch_items if branch_item.is_available]
        return bool(available_items and self.is_available)
