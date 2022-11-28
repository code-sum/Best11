from django.urls import path
from . import views

app_name = "korea"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create_player"),  # 선수 등록
    path("detail/<int:player_pk>", views.detail, name="detail"),  # 선수 디테일 정보
    path("update/<int:player_pk>", views.update, name="update"),  # 선수 정보 수정
    path("delete/<int:player_pk>", views.delete, name="delete"),  # 선주 삭제(대표팀 탈락....ㅠㅠ)
    # path(
    #     "<int:players_pk>/comments/create", views.comment_create, name="comment_create"
    # ),  # 뇌피셜 작성
    # path(
    #     "<int:players_pk>/comments/<int:comment_pk>/update/",
    #     views.comment_update,
    #     name="comment_update",
    # ),  # 뇌피셜 수정
    # path(
    #     "<int:players_pk>/comments/<int:comment_pk>/delete/",
    #     views.comment_delete,
    #     name="comment_delete",
    # ),  # 뇌피셜 삭제
    # path("like/<int:comment_pk>", views.like, name="like"),  # 뇌피셜 좋아요
]
