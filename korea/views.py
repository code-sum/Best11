from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import PlayersForm, CommentForm, BlockForm
from .models import Players, Comment
from sns.models import Sns
from django.db.models import Count


def comment_table(p):
    table = [0] * len(p)
    i = 0
    for j in range(1, len(p)):
        while i > 0 and p[i] != p[j]:
            i = table[i - 1]
        if p[i] == p[j]:
            i += 1
            table[j] = i
    return table


def KMP(p, t):
    ans = []
    table = comment_table(p)
    i = 0
    for j in range(len(t)):
        while i > 0 and p[i] != t[j]:
            i = table[i - 1]
        if p[i] == t[j]:
            if i == len(p) - 1:
                ans.append(j - len(p) + 2)
                i = table[i]
            else:
                i += 1
    return ans


def index(request):
    players = Players.objects.order_by("position")
    fw_players = Players.objects.filter(position="FW")
    mf_players = Players.objects.filter(position="MF")
    df_players = Players.objects.filter(position="DF")
    gk_players = Players.objects.filter(position="GK")
    like_players = Players.objects.annotate(like_count=Count("fans")).order_by(
        "-like_count"
    )[:11]
    like_comments = Comment.objects.annotate(count=Count("like_users")).order_by(
        "-count"
    )[:5]
    context = {
        "players": players,
        "fw_players": fw_players,
        "mf_players": mf_players,
        "df_players": df_players,
        "gk_players": gk_players,
        "like_players": like_players,
        "like_comments": like_comments,
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
    comments = (
        Comment.objects.annotate(count=Count("like_users"))
        .filter(players=player_pk)
        .order_by("-count")
    )

    for t in comments:
        with open("filter.txt", "r", encoding="utf-8") as txtfile:
            for word in txtfile.readlines():
                word = word.strip()
                ans = KMP(word, t.content)
                if ans:
                    for k in ans:
                        k = int(k)
                        if k < len(t.content) // 2:
                            t.content = (
                                len(t.content[k - 1 : len(word)]) * "*"
                                + t.content[len(word) :]
                            )
                        else:
                            t.content = (
                                t.content[0 : k - 1] + len(t.content[k - 1 :]) * "*"
                            )

    sns = Sns.objects.get(pk=player_pk)
    master = str(request.user)
    blocks = Block.objects.filter(players=player)  # 신고한 댓글 목록
    block_list = []
    block_comment = []
    for b in blocks:
        if request.user.pk == b.user.pk:
            block_list.append(b.user.pk)
            block_comment.append(b.comment.pk)

    print(block)
    context = {
        "player": player,
        "master": master,
        "comments": comments,
        "sns": sns,
        "blocks": blocks,
        "block_list": block_list,
        "block_comment": block_comment,
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


# 피셜 생성
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


# 피셜 수정
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


# 피셜 삭제
@login_required
def comment_delete(request, comment_pk, player_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comments = (
        Comment.objects.annotate(count=Count("like_users"))
        .filter(players=player_pk)
        .order_by("-count")
    )
    if request.user.is_authenticated and request.user == comment.user:
        comment.user.exp -= 1
        comment.user.exp -= 2 * comment.like_users.count()
        comment.delete()
        comment.user.save()

    return redirect("korea:detail", player_pk)

# 피셜 좋아요
@login_required
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

# 규칙
def rule(request):
    return render(request, "korea/rule.html")

# 게임 메인
def game(request):
    return render(request, "korea/game.html")

# 1인 게임
def game_1p(request):
    return render(request, "korea/game_1p.html")

# 2인 게임
def game_2p(request):
    return render(request, "korea/game_2p.html")

# 댓글 신고하기
def block(request, player_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    player = Players.objects.get(pk=player_pk)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = BlockForm(request.POST)
            block = Block()
            block.players = player
            block.comment = comment
            block.user = request.user
            block.save()
            is_report = True

        context = {
            "is_report": is_report,
        }

        return JsonResponse(context)

# 경기 일정
def match(request):
    return render(request, "korea/match.html")
