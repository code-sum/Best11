from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import PasswordChangeForm
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    CustomAuthenticationForm,
)
from django.contrib.auth import update_session_auth_hash
from korea.models import Comment, Block, Players
from django.db.models import Count
from django.http import JsonResponse
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST, require_safe
import requests
from bs4 import BeautifulSoup

# 전체 회원관리 페이지(관리자만 접속 가능)
@login_required
def index(request):
    if request.user.is_superuser:
        accounts = get_user_model().objects.order_by("-pk")
        context = {"accounts": accounts}
        return render(request, "accounts/index.html", context)
    else:
        return redirect("korea:index")


# 회원가입 
def signup(request):
    # 이미 로그인된 사람은 korea:index 로 보냄
    if request.user.is_authenticated:
        return redirect("korea:index")
    else:
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return redirect("korea:index")
        else:
            form = CustomUserCreationForm()
        context = {
            "form": form,
        }
        return render(request, "accounts/signup.html", context)


# 로그인
def login(request):
    # 비로그인 상태일 때만 로그인 가능
    if request.user.is_anonymous:
        if request.method == "POST":
            form = CustomAuthenticationForm(request, data=request.POST)
            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect("korea:index")
        else:
            form = CustomAuthenticationForm()
        context = {
            "form": form,
        }
        return render(request, "accounts/login.html", context)
    # 이미 로그인 상태면 korea:index 로 보냄
    else:
        return redirect("korea:index")


# 로그아웃
@login_required
def logout(request):
    auth_logout(request)
    return redirect("korea:index")


# 회원 개인 프로필
def detail(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    comments = (
        user.comment_set.values("players_id")
        .annotate(play=Count("players_id"))
        .order_by("players_id")
    )
    comment_count = len(comments)
    job = "벤치"
    if user.exp < 30:
        job = "벤치"
    elif user.exp >= 30 and user.exp < 80:
        job = "선수"
    elif user.exp >= 80 and comment_count > 12:
        job = "감독"
    else:
        job = "선수"
    context = {
        "user": user,
        "comment_count": comment_count,
        "job": job,
    }
    return render(request, "accounts/detail.html", context)


# 팔로우
@require_POST
def follow(request, pk):
    # 로그인한 사용자만 팔로우 기능 사용 가능
    if request.user.is_authenticated:
        accounts = get_user_model().objects.get(pk=pk)
        comments = (
            accounts.comment_set.values("players_id")
            .annotate(play=Count("players_id"))
            .order_by("players_id")
        )
        comment_count = len(comments)
        if request.user != accounts:
            if request.user in accounts.followers.all():
                accounts.followers.remove(request.user)
                is_followed = False
                accounts.exp -= 1
                accounts.save()
            else:
                accounts.followers.add(request.user)
                is_followed = True
                accounts.exp += 1
                accounts.save()
            context = {
                "is_Followed": is_followed,
                "followers_count": accounts.followers.count(),
                "followings_count": accounts.followings.count(),
                "exp_count": accounts.exp,
                "comment_count": comment_count,
            }
            return JsonResponse(context)
        return redirect('accounts:detail', accounts.username)
    return redirect('accounts:login')
    

# 회원정보 수정
@login_required
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
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("accounts:detail", request.user.pk)
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/change_password.html", context)


# 회원탈퇴
def delete(request, pk):
    if request.user.is_authenticated:
        user = get_object_or_404(get_user_model(), pk=pk)
        if request.user == user:
            request.user.delete()
            auth_logout(request)
        return redirect("korea:index")
    return redirect("accounts:login")


# 피셜피드
@login_required
def special_feed(request, pk):
    user = get_user_model().objects.prefetch_related(
        Prefetch(
            "followings",
            queryset=get_user_model().objects.prefetch_related("comment_set").all(),
            to_attr="followings_users",
        )
    )
    comments = list()
    for followings_user in user.get(pk=request.user.pk).followings_users:
        for comment in followings_user.comment_set.all():
            comments.append(comment)

    comments.sort(key=lambda x: x.created_at, reverse=True)

    # 네이버 뉴스 월드컵 검색 결과(뉴스 페이지)
    url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%9B%94%EB%93%9C%EC%BB%B5'

    r = requests.get(url)
    html = r.content
    # 기사 헤드라인 가져오기
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select('.news_tit')
    list_ = []
    for i in title:
        list_.append(i.text)

    # 기사 a태그 url 가져오기
    soup2 = BeautifulSoup(html, 'html.parser')
    links = soup2.find_all('a', class_='news_tit') # 모든 a 태그 추출
    tag_ = []
    for i in links:
        href = i.attrs['href']
        tag_.append(href)

    dic = { head:value for head, value in zip(list_, tag_)}

    # 좋아요 많이 받은 피셜 가져오기
    like_comments_first = Comment.objects.annotate(count=Count("like_users")).order_by(
        "-count"
    )[0:1]
    like_comments_second = Comment.objects.annotate(count=Count("like_users")).order_by(
        "-count"
    )[1:2]
    like_comments_third = Comment.objects.annotate(count=Count("like_users")).order_by(
        "-count"
    )[2:3]
    like_comments_four = Comment.objects.annotate(count=Count("like_users")).order_by(
        "-count"
    )[3:4]
    like_comments_five = Comment.objects.annotate(count=Count("like_users")).order_by(
        "-count"
    )[4:5]
    

    context = {
        "comments": comments,
        "dic": dic,
        "like_comments_first": like_comments_first,
        "like_comments_second": like_comments_second,
        "like_comments_third": like_comments_third,
        "like_comments_four": like_comments_four,
        "like_comments_five": like_comments_five,
    }
    return render(request, "accounts/special_feed.html", context)


# 신고한 피셜 목록
@login_required
def report(request, pk):
    user = get_user_model().objects.get(pk=pk)
    blocks = Block.objects.filter(user_id=pk)

    context = {
        "user": user,
        "blocks": blocks,
    }

    return render(request, "accounts/report.html", context)


# 신고한 피셜 목록
@login_required
def report_delete(request, pk, comment_pk):
    user = get_user_model().objects.get(pk=pk)
    comment = Comment.objects.get(pk=comment_pk)
    block = Block.objects.get(comment_id=comment_pk)
    block.delete()

    return redirect("accounts:report", pk)
