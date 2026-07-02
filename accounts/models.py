from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    department = models.CharField(max_length=50, blank=True, null=True, verbose_name="部署")
    # 必要に応じて追加予定
    def __str__(self):
        return self.username