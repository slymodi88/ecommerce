import jwt
from django.contrib.auth.base_user import BaseUserManager

from Ecommerce import settings


class UserManager(BaseUserManager):
    def create_user(self, user_name, password=None):
        if not user_name:
            raise ValueError('username required')

        user = self.model(
            user_name=user_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password):
        user = self.create_user(
            user_name,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_token(self, user):
        payload = {'id': user.id, 'user_name': user.user_name}
        token = jwt.encode(
            payload, settings.SECRET_KEY)
        user.token = bytes.decode(token)
        user.save()
        return user


