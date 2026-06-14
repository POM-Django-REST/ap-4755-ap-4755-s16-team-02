from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect

from book.models import Book
from .models import Order
from .forms import OrderForm


def orders_list(request):

    if not request.user.is_authenticated:
        return render(request, "403_forbidden.html")

    if request.user.role == 1:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)

    return render(
        request,
        "order/order_list.html",
        {"orders": orders}
    )

def order_create(request):
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, "403_forbidden.html")

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("orders_list")
    else:
        form = OrderForm()

    return render(request, "order/order_create.html", {"form": form})


def order_close(request, pk):
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, "403_forbidden.html")

    try:
        order = Order.objects.get(id=pk)

        if not order.end_at:
            order.end_at = timezone.now()

            if order.book:
                order.book.count += 1
                order.book.save()

            order.save()

        return redirect("orders_list")

    except Order.DoesNotExist:
        return HttpResponse("Order not found")
    
    
def order_book(request, book_id):
    if not request.user.is_authenticated:
        return render(request, "403_forbidden.html")

    try:
        book = Book.objects.get(id=book_id)

        if book.count <= 0:
            return HttpResponse("Book is not available")

        Order.objects.create(
            user=request.user,
            book=book,
            plated_end_at=timezone.now()
        )

        book.count -= 1
        book.save()

        return redirect("orders_list")

    except Book.DoesNotExist:
        return HttpResponse("Book not found")