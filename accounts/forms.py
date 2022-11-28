from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

# from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "password1",
            "password2",
            "last_name",
            "first_name",
            "profile_image",
        )
        labels = {
            "username": "아이디",
            "last_name": "성",
            "first_name": "이름",
            "profile_image": "프로필 이미지",
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("last_name", "first_name", "profile_image")
        labels = {
            "last_name": "성",
            "first_name": "이름",
            "profile_image": "프로필 이미지 변경",
        }
