from rest_framework import serializers
from .models import Book
from category.serializers import CategorySerializer

class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    discounted_price = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'price', 'discount', 'stock', 
            'status', 'description', 'image_url', 'category', 
            'category_id', 'published_year', 'created_at', 
            'updated_at', 'discounted_price', 'is_available'
        ]
        read_only_fields = ['created_at', 'updated_at']