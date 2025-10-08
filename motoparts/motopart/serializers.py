from rest_framework import serializers
from .models import Motopart
from category.serializers import CategorySerializer

class MotopartSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    discounted_price = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    image_full_url = serializers.ReadOnlyField()
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Motopart
        fields = [
            'id', 'name', 'slug', 'price', 'discount', 'stock',
            'status', 'description', 'image', 'image_url', 'image_full_url',
            'category', 'category_id', 'manufacture_year', 'supplier',
            'created_at', 'updated_at', 'discounted_price', 'is_available'
        ]
        read_only_fields = ['created_at', 'updated_at']