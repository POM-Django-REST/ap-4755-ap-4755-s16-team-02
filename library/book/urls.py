from django.urls import path
from . import views
from .views import BookApiView, BookListApiView

urlpatterns = [
    # path('', views.book_list, name='book_list'),
    path('', BookListApiView.as_view()),
    path('<int:id>/',BookApiView.as_view()),
    path('create/', views.book_create, name='book_create'),
    path('<int:book_id>/update/', views.book_update, name='book_update'),
    path("<int:book_id>/delete/", views.book_delete, name="book_delete"),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('user/<int:user_id>/', views.user_books, name='user_books'),
]