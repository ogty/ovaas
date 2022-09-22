from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    token = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
