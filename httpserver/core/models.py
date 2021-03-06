from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class URL(models.Model):
    url = models.CharField(max_length=2048)
    timestamp = models.DateTimeField()
    content = models.TextField()
