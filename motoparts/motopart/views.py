from django.shortcuts import render
from .models import Motopart
from rest_framework import generics
from .serializers import MotopartSerializer

class MotopartListView(generics.ListCreateAPIView):
    queryset = Motopart.objects.all()
    serializer_class = MotopartSerializer

# Create your views here.
