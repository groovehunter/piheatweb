
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    username    = models.CharField(max_length=40, unique=True)
    dt_added    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
