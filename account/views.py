from django.db import IntegrityError
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect

from .utils.token import generate_random_token
from .utils.commands import create_function, delete_function, deploy
from .models import CustomUser


def index(request: HttpRequest) -> HttpRequest:
    if request.method == "POST" and request.user.is_authenticated:
        zipped_file = request.FILES["zip"]
        with open(f"media/{request.user.token}.zip", "wb+") as destination:
            for chunk in zipped_file.chunks():
                destination.write(chunk)
        deploy(request.user.token, request.user.username)

    return render(request, "index.html", {})


def signup(request: HttpRequest) -> HttpRequest | HttpResponseRedirect:
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = CustomUser.objects.create_user(username=username, password=password)
            user.token = generate_random_token()
            user.save()

            create_function(username)
            django_login(request, user)

            return redirect('/')
        except IntegrityError:
            return render(request, "signup.html", {"error": "Username already exists"})

    return render(request, "signup.html", {})


def login(request: HttpRequest) -> HttpRequest | HttpResponseRedirect:
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, "login.html", {"error": "Invalid username or password"})

        django_login(request, user)
        user = CustomUser.objects.get(username=username)
        return redirect('/')

    return render(request, "login.html", {})


def logout(request: HttpRequest) -> HttpResponseRedirect:
    django_logout(request)
    return redirect("/login")


def delete_user(request: HttpRequest) -> HttpResponseRedirect:
    delete_function(request.user.username)
    request.user.delete()
    return redirect('/')
