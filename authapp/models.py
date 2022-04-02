from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class ApiUser(AbstractUser):
    # uid = models.UUIDField(primary_key=True, default=uuid4(), null=False)
    add_datetime = models.DateTimeField(verbose_name='был создан', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name='был изменен', auto_now=True)
    email = models.EmailField(unique=True)
