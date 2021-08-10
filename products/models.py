from django.db import models
from django.db.models import F, Min

from helpers.models import Timestamps


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Product(Timestamps):
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    is_available = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    image = models.ImageField()
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField("Category")

    def __str__(self):
        return self.title
