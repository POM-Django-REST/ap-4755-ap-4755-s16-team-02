from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .models import CustomUser
from .forms import LoginForm, RegisterForm, UserUpdateForm


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = CustomUser.objects.filter(email=email).first()

            if user and user.check_password(password):
                login(request, user)
                return redirect("home")

            form.add_error(None, "Неправильний email або пароль")
    else:
        form = LoginForm()

    return render(request, "authentication/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "authentication/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


def user_list(request):
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, "403_forbidden.html")

    users = CustomUser.objects.all()
    return render(request, "authentication/user_list.html", {"users": users})


def user_detail(request, user_id):
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, "403_forbidden.html")

    user_obj = get_object_or_404(CustomUser, id=user_id)
    return render(request, "authentication/user_detail.html", {"user_obj": user_obj})

def user_update(request, user_id):
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, "403_forbidden.html")

    user_obj = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user_obj)

        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = UserUpdateForm(instance=user_obj)

    return render(request, "authentication/user_update.html", {"form": form})


def user_delete(request, user_id):
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, "403_forbidden.html")

    user_obj = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        user_obj.delete()
        return redirect("user_list")

    return render(request, "authentication/user_delete.html", {"user_obj": user_obj})