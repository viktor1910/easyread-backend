from rest_framework import serializers
from .models import OrderItem
from book.models import Book
from orders.models import Order

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model"""
    
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author.name', read_only=True)
    order_id = serializers.IntegerField(source='order.id', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'order_id', 'book', 'book_title', 'book_author',
            'quantity', 'unit_price', 'total', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total', 'created_at', 'updated_at']

class OrderItemCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating OrderItem"""
    
    class Meta:
        model = OrderItem
        fields = ['order', 'book', 'quantity', 'unit_price']
    
    def validate(self, data):
        """Validate order item data"""
        order = data.get('order')
        book = data.get('book')
        quantity = data.get('quantity', 1)
        
        # Check if order exists and belongs to user
        if not order:
            raise serializers.ValidationError("Order is required")
        
        # Check if book exists
        if not book:
            raise serializers.ValidationError("Book is required")
        
        # Use book price as unit_price if not provided
        if 'unit_price' not in data or data['unit_price'] is None:
            data['unit_price'] = book.price
        
        # Validate quantity
        if quantity <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        
        return data

class OrderItemUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating OrderItem"""
    
    class Meta:
        model = OrderItem
        fields = ['quantity', 'unit_price']
    
    def validate_quantity(self, value):
        """Validate quantity"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
    
    def validate_unit_price(self, value):
        """Validate unit price"""
        if value <= 0:
            raise serializers.ValidationError("Unit price must be greater than 0")
        return value

class OrderItemListSerializer(serializers.ModelSerializer):
    """Serializer for listing OrderItems with minimal data"""
    
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'book', 'book_title', 'book_author',
            'quantity', 'unit_price', 'total'
        ]
