from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'korea/index.html')
