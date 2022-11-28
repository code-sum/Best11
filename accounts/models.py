from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.


class User(AbstractUser):
    # 팔로우, 팔로잉
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    # 프로필 이미지
    profile_image = ProcessedImageField(
        upload_to="media/",
        blank=True,
        processors=[ResizeToFill(360, 360)],
        format="JPEG",
        options={"quality": 80},
    )
    # 활동지수(벤치/선수/감독)
    exp = models.IntegerField(default=0)
