from django.urls import path
from book.views import BookApiView, BookListApiView
from author.views import AuthorApiView, AuthorListApiView

urlpatterns = [
    path('book/',BookListApiView.as_view()),
    path('book/<int:id>/', BookApiView.as_view()),
    path('author/', AuthorListApiView.as_view()),
    path('author/<int:id>/', AuthorApiView.as_view()),
]