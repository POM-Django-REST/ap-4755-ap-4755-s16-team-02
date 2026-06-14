from django.urls import path
from .views import orders_list, order_create, order_close, order_book

urlpatterns = [
    path("", orders_list, name="orders_list"),
    path("create/", order_create, name="order_create"),
    path("<int:pk>/close/", order_close, name="order_close"),
    path("book/<int:book_id>/", order_book, name="order_book"),
]