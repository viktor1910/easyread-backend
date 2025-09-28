from django.shortcuts import render
from .models import Category
from rest_framework import generics
from .serializers import CategorySerializer

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Create your views here.
