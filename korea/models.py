from django.db import models
from django.conf import settings

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.


class Players(models.Model):
    name = models.CharField(max_length=7)
    english_name = models.CharField(max_length=20)
    back_number = models.IntegerField()
    birthdate = models.DateField()
    team = models.CharField(max_length=20)
    player_image = ProcessedImageField(
        upload_to="",
        blank=True,
        processors=[ResizeToFill(200, 200)],
        format="JPEG",
        options={"quality": 80},
    )
    position = models.CharField(max_length=10)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    fans = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, related_name="like_player"
    )

    def profile_image(self):
        if self.player_image and hasattr(self.player_image, "url"):
            return self.player_image.url
        else:
            return "../static/images/Soccer-Ball.png"


class Comment(models.Model):  # 선수 한 명에 대한 뇌피셜
    players = models.ForeignKey(
        Players, on_delete=models.CASCADE
    )  # 선수를 ForeignKey로 불러온다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        # elif time < timedelta(days=2):
        #     time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
        #     return str(time.days) + '일 전'
        else:
            return False