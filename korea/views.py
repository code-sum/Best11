from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import PlayersForm
from .models import Players


def index(request):
    players = Players.objects.all()

    context = {"players": players}

    return render(request, "korea/index.html", context)


# 선수단 생성 Create(관리자만 생성 가능)
def create(request):
    if request.method == "POST":
        form = PlayersForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("korea:index")

    else:
        form = PlayersForm()
    context = {"form": form}
    return render(request, "korea/create_player.html", context)


# 선수 디테일 정보
def detail(request, player_pk):
    player = Players.objects.get(pk=player_pk)
    context = {"player": player}
    return render(request, "korea/detail_player.html", context)


def update(request, player_pk):
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


def delete(request, player_pk):
    player = Players.objects.get(pk=player_pk)
    player.delete()
    return redirect("korea:index")
