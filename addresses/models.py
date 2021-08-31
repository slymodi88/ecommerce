from helpers.models import Timestamps
from django.contrib.gis.db import models


class Address(Timestamps):
    """
    store user location data
    """
    title = models.CharField(max_length=255, default='home')
    city = models.ForeignKey('branches.City', on_delete=models.CASCADE, default=1)
    location = models.PointField(default=None)
    address_info = models.TextField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.address_info
