from rest_framework import serializers
from .models import CartItem
from book.serializers import BookSerializer

class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    unit_price = serializers.ReadOnlyField()
    total = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'cart', 'book', 'book_id', 'quantity', 
            'unit_price', 'total', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'cart']

class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['book_id', 'quantity']
        
    def create(self, validated_data):
        # Automatically assign the cart from context
        validated_data['cart'] = self.context['cart']
        return super().create(validated_data)
        
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
