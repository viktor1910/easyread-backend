from django.shortcuts import render
from .models import Book
from rest_framework import generics
from .serializers import BookSerializer

class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Create your views here.
