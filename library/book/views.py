from django.shortcuts import render, get_object_or_404, redirect

from .models import Book
from .forms import BookForm
from order.models import Order
from authentication.models import CustomUser


def book_list(request):
    """Список всіх книг + фільтрація"""

    books = Book.objects.all()

    search_title = request.GET.get("title", "").strip().lower()
    search_author = request.GET.get("author", "").strip().lower()

    if search_title:
        books = books.filter(name__icontains=search_title)

    if search_author:
        books = [
            book for book in books
            if any(
                search_author in author.name.lower()
                or search_author in author.surname.lower()
                or search_author in author.patronymic.lower()
                for author in book.authors.all()
            )
        ]

    return render(
        request,
        "book/book_list.html",
        {"books": books}
    )


def book_detail(request, book_id):
    """Деталі конкретної книги"""

    book = get_object_or_404(Book, id=book_id)

    return render(
        request,
        "book/book_detail.html",
        {"book": book}
    )


def user_books(request, user_id):
    """Книги, видані конкретному юзеру (тільки для бібліотекаря)"""

    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, "403_forbidden.html")

    target_user = get_object_or_404(CustomUser, id=user_id)

    orders = Order.objects.filter(user=target_user)

    return render(
        request,
        "book/user_books.html",
        {
            "orders": orders,
            "target_user": target_user
        }
    )


def book_create(request):
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, "403_forbidden.html")

    if request.method == "POST":
        form = BookForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()

    return render(
        request,
        "book/book_create.html",
        {"form": form}
    )


def book_update(request, book_id):
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, "403_forbidden.html")

    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = BookForm(
            request.POST,
            instance=book
        )

        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)

    return render(
        request,
        "book/book_update.html",
        {"form": form}
    )


def book_delete(request, book_id):
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, "403_forbidden.html")

    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        book.delete()
        return redirect("book_list")

    return render(
        request,
        "book/book_delete.html",
        {"book": book}
    )