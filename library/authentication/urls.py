from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    user_list,
    user_detail,
    user_update,
    user_delete,
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("users/", user_list, name="user_list"),
    path("users/<int:user_id>/", user_detail, name="user_detail"),
    path("users/<int:user_id>/update/", user_update, name="user_update"),
    path("users/<int:user_id>/delete/", user_delete, name="user_delete"),
]