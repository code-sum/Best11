from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

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
    password = ReadOnlyPasswordHashField(
        label=(""),
        help_text=''
        )
    class Meta:
        model = get_user_model()
        fields = ("last_name", "first_name", "profile_image")
        labels = {
            "last_name": "성",
            "first_name": "이름",
            "profile_image": "프로필 이미지 변경",
        }

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
                        'placeholder':'아이디'})
        for fieldname in ['username']:
            self.fields[fieldname].label = ''

        self.fields['password'].widget.attrs.update({
                        'placeholder':'비밀번호'})
        for fieldname in ['password']:
            self.fields[fieldname].label = ''