from django.shortcuts import render
from .models import Motopart
from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from .serializers import MotopartSerializer
from .pagination import MotopartPagination
from user.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

class MotopartListView(generics.ListCreateAPIView):
    queryset = Motopart.objects.all()
    serializer_class = MotopartSerializer
    pagination_class = MotopartPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'manufacture_year', 'supplier']
    search_fields = ['name', 'description', 'supplier']
    ordering_fields = ['name', 'price', 'discounted_price', 'stock', 'manufacture_year', 'created_at']
    ordering = ['-created_at']  # Default ordering

    def get_permissions(self):
        """
        GET: public (AllowAny)
        POST: admin only
        """
        if self.request.method == 'POST':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class MotopartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Motopart.objects.all()
    serializer_class = MotopartSerializer
    lookup_field = 'pk'  # Can use 'slug' if you prefer slug-based lookups

    def get_permissions(self):
        """
        GET: public (AllowAny)
        PUT/PATCH/DELETE: admin only
        """
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

# Create your views here.
