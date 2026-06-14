from django.shortcuts import render
from book.models import Book
from author.models import Author
from order.models import Order


def home(request):
    context = {
        "books_count": Book.objects.count(),
        "authors_count": Author.objects.count(),
        "orders_count": Order.objects.filter(end_at__isnull=True).count(),
    }

    return render(request, "home.html", context)