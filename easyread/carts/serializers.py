from rest_framework import serializers
from .models import Cart
from cartitem.models import CartItem
from cartitem.serializers import CartItemSerializer

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.ReadOnlyField()
    items_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'status', 'created_at', 'updated_at',
            'items', 'subtotal', 'items_count'
        ]
        read_only_fields = ['created_at', 'updated_at', 'user']

class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['status']
        
    def create(self, validated_data):
        # Automatically assign the current user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
