from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AuthorSerializer

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



# class AuthorListApiView(APIView):
#     def get(self, request):
#         try:
#             id = request.query_params['id']
#             author = Author.objects.get(pk=id)
#             serializer = AuthorSerializer(author)
#         except:
#             authors = Author.objects.all()
#             serializer = AuthorSerializer(authors, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         data = {
#             'name': request.data.get('name'),
#             'surname': request.data.get('surname'),
#             'patronymic': request.data.get('patronymic')
#         }
#         serializer = AuthorSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, id):
#         try:
#             author = Author.objects.get(pk=id)
#         except Author.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         author.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     def put(self, request, id):
#         author = Author.objects.get(pk=id)
#         serializer = AuthorSerializer(author, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorListApiView(APIView):
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = {
            'name': request.data.get('name'),
            'surname': request.data.get('surname'),
            'patronymic': request.data.get('patronymic')
        }
        
        serializer = AuthorSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class AuthorApiView(APIView):
    def get(self, request, id):
        try:
            author = Author.objects.get(pk=id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = AuthorSerializer(author)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        try:
            author = Author.objects.get(pk=id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = AuthorSerializer(author, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            author = Author.objects.get(pk=id)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)