from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Author
from .forms import AuthorForm

def authors_list(request):
    authors = Author.objects.all()
    return render(request, "author/authors_list.html", {"authors": authors})


def author_create(request):
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, "403_forbidden.html")
    if request.method == "POST":
        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("authors_list")
    else:
        form = AuthorForm()

    return render(request, "author/author_create.html", {"form": form})


def author_delete(request, pk):
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, "403_forbidden.html")
    author = get_object_or_404(Author, id=pk)

    if author.books.count() == 0:
        author.delete()
        messages.success(request, "Автор успішно видалений.")
    else:
        messages.error(request, "Неможливо видалити автора, бо у нього є книги.")

    return redirect("authors_list")
    
def author_update(request, pk):
    if not request.user.is_authenticated or request.user.role != 1:
        return render(request, "403_forbidden.html")
    author = get_object_or_404(Author, id=pk)

    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)

        if form.is_valid():
            form.save()
            return redirect("authors_list")
    else:
        form = AuthorForm(instance=author)

    return render(request, "author/author_update.html", {"form": form})