from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
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

    def clean(self):
        """入力データの整合性チェック"""
        super().clean()

        # 1. 過去の日付でないかチェック
        if self.date < timezone.now().date():
            raise ValidationError("過去の日付で予約することはできません。")

        # 2. 開始時間が終了時間より前かチェック
        if self.start_time >= self.end_time:
            raise ValidationError("終了時間は開始時間よりも後の時刻にしてください。")

        # 3. 重複チェック（同じ会議室、同じ日、時間が重なっているもの）
        # ロジック: (既存の開始 < 入力の終了) AND (既存の終了 > 入力の開始)
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            date=self.date
        ).exclude(pk=self.pk)  # 自分自身（編集時）は除外

        for existing in overlapping_bookings:
            if (self.start_time < existing.end_time) and (self.end_time > existing.start_time):
                raise ValidationError(
                    f"指定された時間は既に予約が入っています。({existing.start_time} - {existing.end_time})"
                )