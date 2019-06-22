import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class BaseUser(PermissionsMixin,
               AbstractBaseUser):

    username = models.CharField(unique=True, max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    secret_key = models.UUIDField(default=uuid.uuid4, unique=True)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return 'User: {0}'.format(self.username)

    def rotate_secret_key(self):
        self.secret_key = uuid.uuid4()
        self.save()
