from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import PlayersForm, CommentForm

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

# 뇌피셜 작성
def comment_create(request):
    # player = Players.objects.get(pk=pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit = False)
            comment.save()
            return redirect('korea:detail_player')
    else:
        comment_form = CommentForm()
    context = {
        'comment_form': comment_form,
    }
    return render(request, "korea/comment_create.html", context)

# 뇌피셜 좋아요
def like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user in comment.like_users.all():
        # 좋아요 삭제하고
        comment.like_users.remove(request.user)
        is_liked = False
    else:  # 좋아요 누르지 않은 상태라면 좋아요에 추가하고
        comment.like_users.add(request.user)
        is_liked = True
        # 상세 페이지로 redirect
    context = {"isLiked": is_liked, "likeCount": comment.like_users.count()}
    return JsonResponse(context)