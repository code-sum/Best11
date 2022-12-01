from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import PlayersForm, CommentForm
from .models import Players


def index(request):
    players = Players.objects.order_by("english_name")
    fw_players = Players.objects.filter(position="FW")
    mf_players = Players.objects.filter(position="MF")
    df_players = Players.objects.filter(position="DF")
    gk_players = Players.objects.filter(position="GK")
    
    context = {
        "players": players,
        "fw_players": fw_players,
        "mf_players": mf_players,
        "df_players": df_players,
        "gk_players": gk_players
        }

    return render(request, "korea/index.html", context)


# 선수단 생성 Create(관리자만 생성 가능)
def create(request):
    if str(request.user) == "admin":
        if request.method == "POST":
            form = PlayersForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect("korea:index")

        else:
            form = PlayersForm()
        context = {"form": form}
        return render(request, "korea/create_player.html", context)
    else:
        return redirect("korea:index")


# 선수 디테일 정보
def detail(request, player_pk):
    player = Players.objects.get(pk=player_pk)
    comments = player.comment_set.all().order_by('-pk')  
    
    print(comments)
    master = str(request.user)
    context = {
        "player": player,
        "master": master,
        "comments": comments,
    }
    return render(request, "korea/detail_player.html", context)


# 선수단 정보 업데이트(관리자만 생성 가능)
def update(request, player_pk):
    if str(request.user) == "admin":
        player = Players.objects.get(pk=player_pk)
        if request.method == "POST":
            player_form = PlayersForm(request.POST, request.FILES, instance=player)
            if player_form.is_valid():
                form = player_form.save(commit=False)
                form.save()
                return redirect("korea:detail", player_pk)
        else:
            player_form = PlayersForm(instance=player)
        context = {
            "player_form": player_form,
            "player": player,
        }
        return render(request, "korea/update_player.html", context)
    else:
        return redirect("korea:index")


# 선수단 삭제(관리자만 생성 가능)
def delete(request, player_pk):
    if str(request.user) == "admin":
        player = Players.objects.get(pk=player_pk)
        player.delete()
        return redirect("korea:index")
    else:
        return redirect("korea:index")


# 선수 좋아요
@login_required
def like_player(request, player_pk):
    if request.user.is_authenticated:
        player = Players.objects.get(pk=player_pk)
        if player.fans.filter(pk=request.user.pk).exists():
            player.fans.remove(request.user)
            is_likeds = False
        else:
            player.fans.add(request.user)
            is_likeds = True
        return JsonResponse(
            {
                "is_likeds": is_likeds,
                "like_count": player.fans.count(),
            }
        )
    else:
        return redirect("korea:detail", player_pk)


# 뇌피셜 생성
@login_required
def comment_create(request, player_pk):
    player = Players.objects.get(pk=player_pk)
    if request.method == "POST":
        comment_form = CommentForm(
            request.POST, request.FILES
        )  # instance=player 불필요한 argument임!
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.players = player
            # print(comment.players)
            comment.user = request.user
            user = comment.user
            user.exp += 1
            user.save()
            comment.save()
            return redirect("korea:detail", player_pk)
    else:
        comment_form = CommentForm()
    context = {
        "comment_form": comment_form,
        "player": player,
    }
    return render(request, "korea/comment_create.html", context)


# 뇌피셜 수정
@login_required
def comment_update(request, player_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        if request.method == "POST":
            comment_form = CommentForm(request.POST, request.FILES, instance=comment)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.save()  # 자나깨나 save
                return redirect("korea:detail", player_pk)
        else:
            comment_form = CommentForm(instance=comment)
        context = {
            "comment_form": comment_form,
            "comment": comment,
        }
        return render(request, "korea/comment_update.html", context)
    return redirect("korea:detail", player_pk)


# 뇌피셜 삭제
@login_required
def comment_delete(request, comment_pk, player_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user.is_authenticated and request.user == comment.user:
        comment.delete()
    return redirect("korea:detail", player_pk)


# 뇌피셜 좋아요
def likes(request, player_pk, comment_pk):
    player = Players.objects.get(pk=player_pk)
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk=comment_pk)
        if request.user in comment.like_users.all():
            comment.like_users.remove(request.user)
            is_liked = False
            comment.user.exp -= 2
            comment.user.save()

        else:
            comment.like_users.add(request.user)
            is_liked = True
            comment.user.exp += 2
            comment.user.save()
        context = {
            "is_liked": is_liked,
            "likeCount": comment.like_users.count(),
        }
        return JsonResponse(context)
        # return redirect("korea:detail", player_pk)

    # player = Players.objects.get(pk=player_pk)
    # if request.user.is_authenticated:
    #     comment = Comment.objects.get(pk=comment_pk)
    #     if comment.like_users.filter(pk=request.user.pk).exists():
    #         comment.like_users.remove(request.user)
    #         is_liked= False
    #     else:
    #         comment.like_users.add(request.user)
    #         is_liked= True
    #     context= {
    #         'is_liked': is_liked,
    #         'player': player,
    #         }
    #     return JsonResponse(context)
    # return redirect('accounts:login')