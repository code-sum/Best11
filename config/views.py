from django.shortcuts import render, redirect


def index(request):
    if request.user.is_anonymous:
        return render(request, 'main.html')
    else:
        return redirect("korea:index")
