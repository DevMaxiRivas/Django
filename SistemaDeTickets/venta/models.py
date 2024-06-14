from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Añade campos adicionales aquí si los necesitas
    pass


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        permissions = [
            ("can_publish", "Can publish articles"),
            ("can_edit", "Can edit articles"),
        ]
