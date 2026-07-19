
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("home")

        return render(
            request,
            "accounts/login.html",
            {
                "error": "Usuario o contraseña incorrectos."
            }
        )

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def register_view(request):
    return render(request, "accounts/register.html")