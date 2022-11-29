from django.urls import path
from . import views

app_name = "korea"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create_player"),  # 선수 등록
    path("detail/<int:player_pk>", views.detail, name="detail"),  # 선수 디테일 정보
    path("update/<int:player_pk>", views.update, name="update"),  # 선수 정보 수정
    path("delete/<int:player_pk>", views.delete, name="delete"),  # 선수 삭제(대표팀 탈락....ㅠㅠ)
    path(
        "like_player/<int:player_pk>", views.like_player, name="like_player"
    ),  # 선수 좋아요(찜하기)
    path('detail/<int:player_pk>/comments/', views.comment_create, name='comment_create'), # 뇌피셜 작성
    path('detail/<int:player_pk>/<int:comment_pk>/update/', views.comment_update, name='comment_update'), # 뇌피셜 수정
    path('detail/<int:player_pk>/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'), # 뇌피셜 삭제
    path('detail/<int:player_pk>/<int:comment_pk>/likes/', views.likes, name='likes'), # 뇌피셜 좋아요
]
