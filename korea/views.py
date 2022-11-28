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

    return render(request, "korea/detail.html")
