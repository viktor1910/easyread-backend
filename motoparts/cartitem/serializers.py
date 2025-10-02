from rest_framework import serializers
from .models import CartItem
from motopart.serializers import MotopartSerializer

class CartItemSerializer(serializers.ModelSerializer):
    motopart = MotopartSerializer(read_only=True)
    motopart_id = serializers.IntegerField(write_only=True)
    unit_price = serializers.ReadOnlyField()
    total = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'cart', 'motopart', 'motopart_id', 'quantity', 
            'unit_price', 'total', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'cart']

class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['motopart_id', 'quantity']
        
    def create(self, validated_data):
        # Automatically assign the cart from context
        validated_data['cart'] = self.context['cart']
        return super().create(validated_data)
        
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
