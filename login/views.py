import bcrypt
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from .forms import UserLoginForm, UserRegisterForm


def index(request):
    form = UserLoginForm
    return render(request, "login/login.html", {"form": form})


def logging(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("polls:index"))
        form = UserLoginForm
        return render(request, "login/login.html", {"error_message": ["Wrong username or password!"], "form": form})
    return HttpResponseRedirect(reverse("login:index"))
        

def register(request):
    form = UserRegisterForm()
    return render(request, "login/register.html", {"form": form})


def reg_new_user(request):
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password1"]
    rep_password = request.POST["password2"]

    error_message = []
    try:
        User.objects.get(username=username)
        error_message.append("User with this username is already registered")
    except User.DoesNotExist:
        try:
            User.objects.get(email=email)
            error_message.append("User with this login is already registered")
        except User.DoesNotExist:
            pass

    if len(username) < 6:
        error_message.append("Username should be at least 6 characters")
    if len(password) < 8:
        error_message.append("Password should contain at least 8 characters")
    if password != rep_password:
        error_message.append("Passwords should be the same")

    if len(error_message):
        return render(request, "login/register.html", {"error_message": error_message})

    User.objects.create_user(username, email, password)

    return HttpResponseRedirect(reverse("login:index"))


def logout_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("polls:index"))
    logout(request)
    return HttpResponseRedirect(reverse("polls:index"))

