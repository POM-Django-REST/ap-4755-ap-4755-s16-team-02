from rest_framework import serializers

from .models import Book
from author.models import Author

class BookSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    
    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors']
        
       