from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    motoparts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'created_at', 'updated_at', 'motoparts_count']
        read_only_fields = ['created_at', 'updated_at']

    def get_motoparts_count(self, obj):
        """Get the count of motoparts in this category"""
        return obj.motoparts.filter(status='active').count()

    