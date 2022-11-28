from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),  # 회원목록(수정 필요)
    path("signup/", views.signup, name="signup"),  # 회원가입
    path("login/", views.login, name="login"),  # 로그인
    path("logout/", views.logout, name="logout"),  # 로그아웃
    path("detail/<int:pk>/", views.detail, name="detail"),  # 내정보
    path("<int:pk>/follow/", views.follow, name="follow"),  # 팔로우
    path("update/", views.update, name="update"),  # 정보수정
    path("password/", views.change_password, name="change_password"),  # 비밀번호 변경
    path("delete/", views.delete, name="delete"),  # 탈퇴
]
