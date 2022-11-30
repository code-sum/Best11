from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import update_session_auth_hash
from korea.models import Comment
from django.db.models import Count

# 회원 목록(변경필요)
def index(request):
    accounts = get_user_model().objects.order_by("-pk")
    context = {"accounts": accounts}
    return render(request, "accounts/index.html", context)


# 회원가입
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("accounts:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


# 로그인
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # 주소 수정 필요
            return redirect(request.GET.get("next") or "accounts:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


# 로그아웃
def logout(request):
    auth_logout(request)
    return redirect("korea:index")


# 회원 정보
def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    comments = (
        user.comment_set.values("players_id")
        .annotate(play=Count("players_id"))
        .order_by("players_id")
    )   
    # comments = (
    #     comments_user.values_list("players_id", flat=True).distinct().order_by("pk")
    # )

    # comment_list = []
    # for comment in comments:
    #     if comment.user.pk == pk:
    #         comment_list.append(comment)
    comment_count = len(comments)
    print(comment_count)
    context = {
        "user": user,
        "comment_count": comment_count,
    }
    return render(request, "accounts/detail.html", context)


# 팔로우
def follow(request, pk):
    accounts = get_user_model().objects.get(pk=pk)
    if request.user == accounts:
        return redirect("accounts:detail", pk)
    if request.user in accounts.followers.all():
        accounts.followers.remove(request.user)
        accounts.exp -= 1
        accounts.save()
    else:
        accounts.followers.add(request.user)
        accounts.exp += 1
        accounts.save()
    return redirect("accounts:detail", pk)


# 회원 정보 수정
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:detail", request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


# 회원 비밀번호 변경
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("accounts:index")
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/change_password.html", context)


# 회원 삭제
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect("accounts:index")
