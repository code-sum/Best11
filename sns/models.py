from django.db import models
from korea.models import Players

# Create your models here.
class Sns(models.Model):
    players = models.ForeignKey(
        Players, on_delete=models.CASCADE
    )  # 선수를 ForeignKey로 불러온다.
    sns_url = models.TextField()
