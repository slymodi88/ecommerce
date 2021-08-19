from django.contrib.auth.models import PermissionsMixin
from users.manager import UserManager
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model is used to hold information about employees that uses the system such as  username, password,email and phonenumber

    """
    user_name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=255)
    token = models.CharField(max_length=255, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    address = models.ForeignKey('locations.Location', on_delete=models.CASCADE, default=1)

    USERNAME_FIELD = 'user_name'
    objects = UserManager()
