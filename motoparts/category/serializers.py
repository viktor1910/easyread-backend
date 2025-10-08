from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    motoparts_count = serializers.SerializerMethodField()
    image_full_url = serializers.ReadOnlyField()
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'image_full_url', 'created_at', 'updated_at', 'motoparts_count']
        read_only_fields = ['created_at', 'updated_at']

    def get_motoparts_count(self, obj):
        """Get the count of motoparts in this category"""
        return obj.motoparts.filter(status='active').count()

