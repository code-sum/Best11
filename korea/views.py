from django.shortcuts import render, redirect
from .forms import PlayersForm


def index(request):
    return render(request, "korea/index.html")


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
