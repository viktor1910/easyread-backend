from django.shortcuts import render
from .models import Category
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import CategorySerializer
from user.permissions import IsAdminUser

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        """
        GET: Không cần permission (public access)
        POST: Chỉ admin mới được tạo category
        """
        if self.request.method == 'POST':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]  # GET method - public access
        return [permission() for permission in permission_classes]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        """
        GET: Không cần permission (public access)
        PUT/PATCH/DELETE: Chỉ admin mới được cập nhật/xóa
        """
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]  # GET method - public access
        return [permission() for permission in permission_classes]


# Create your views here.
