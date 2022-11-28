from django.db import models
from django.conf import settings

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

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
        processors=[ResizeToFill(100, 100)],
        format="JPEG",
        options={"quality": 80},
    )
    position = models.CharField(max_length=10)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    # fans = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name="like_player")

    def profile_image(self):
        if self.player_image and hasattr(self.player_image, "url"):
            return self.player_image.url
        else:
            return "https://postfiles.pstatic.net/MjAyMDExMDFfMTA1/MDAxNjA0MjI4ODc1Mzk0.05ODadJdsa3Std55y7vd2Vm8kxU1qScjh5-3eVJ9T-4g.h7lHansSdReVq7IggiFAc44t2W_ZPTPoZWihfRMB_TYg.JPEG.gambasg/%EC%9C%A0%ED%8A%9C%EB%B8%8C_%EA%B8%B0%EB%B3%B8%ED%94%84%EB%A1%9C%ED%95%84_%ED%8C%8C%EB%9E%91.jpg?type=w773"

class Comment(models.Model): # 선수 한 명에 대한 뇌피셜
    players = models.ForeignKey(Players, on_delete=models.CASCADE) # 선수를 ForeignKey로 불러온다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_comments")