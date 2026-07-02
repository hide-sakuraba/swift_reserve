from django.db import models
from django.conf import settings
# Create your models here.

class Room(models.Model):
    """会議室モデル"""
    name = models.CharField(max_length=100, verbose_name="会議室名")
    capacity = models.PositiveIntegerField(verbose_name="定員")
    location = models.CharField(max_length=100, blank=True, verbose_name="場所・フロア")
    description = models.TextField(blank=True, verbose_name="説明・設備")
    image = models.ImageField(upload_to='rooms/', blank=True, null=True, verbose_name="会議室画像")

    def __str__(self):
        return self.name


class Booking(models.Model):
    """予約モデル"""
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="会議名")
    start_time = models.DateTimeField(verbose_name="開始時間")
    end_time = models.DateTimeField(verbose_name="終了時間")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room.name} - {self.title}"