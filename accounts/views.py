from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect


def login_view(request):

    if request.method == "POST":

        # Antes: request.POST["username"] -> KeyError (error 500) si
        # faltaba el campo en el formulario.
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            next_url = request.POST.get("next") or request.GET.get("next") or "home"
            return redirect(next_url)

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

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")

        errors = []

        if not username or not password:
            errors.append("Usuario y contraseña son obligatorios.")

        elif password != password2:
            errors.append("Las contraseñas no coinciden.")

        elif User.objects.filter(username=username).exists():
            errors.append("Ese nombre de usuario ya existe.")

        # Antes: create_user() se llamaba directo con la contraseña tal
        # cual, sin pasar por validate_password() -> los validadores
        # configurados en AUTH_PASSWORD_VALIDATORS (longitud mínima,
        # contraseñas comunes, similitud con el usuario, etc.) nunca se
        # aplicaban en el registro.
        if not errors and password:
            try:
                validate_password(
                    password,
                    user=User(username=username, email=email),
                )
            except ValidationError as exc:
                errors.extend(exc.messages)

        if errors:
            return render(
                request,
                "accounts/register.html",
                {
                    "errors": errors,
                    "username": username,
                    "email": email,
                }
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        login(request, user)
        return redirect("home")

    return render(request, "accounts/register.html")
