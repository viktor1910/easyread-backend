from rest_framework import serializers
from .models import OrderItem
from motopart.models import Motopart
from orders.models import Order

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model"""
    
    motopart_name = serializers.CharField(source='motopart.name', read_only=True)
    order_id = serializers.IntegerField(source='order.id', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'order_id', 'motopart', 'motopart_nam',
            'quantity', 'unit_price', 'total', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total', 'created_at', 'updated_at']

class OrderItemCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating OrderItem"""
    
    class Meta:
        model = OrderItem
        fields = ['order', 'motopart', 'quantity', 'unit_price']
    
    def validate(self, data):
        """Validate order item data"""
        order = data.get('order')
        motopart = data.get('motopart')
        quantity = data.get('quantity', 1)
        
        # Check if order exists and belongs to user
        if not order:
            raise serializers.ValidationError("Order is required")
        
        # Check if motopart exists
        if not motopart:
            raise serializers.ValidationError("Motopart is required")
        
        # Use motopart price as unit_price if not provided
        if 'unit_price' not in data or data['unit_price'] is None:
            data['unit_price'] = motopart.price
        
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
    
    motopart_title = serializers.CharField(source='motopart.title', read_only=True)
    motopart_brand = serializers.CharField(source='motopart.brand.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'motopart', 'motopart_title', 'motopart_brand',
            'quantity', 'unit_price', 'total'
        ]
