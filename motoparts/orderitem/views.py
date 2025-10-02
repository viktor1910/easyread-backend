from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import OrderItem
from .serializers import (
    OrderItemSerializer, 
    OrderItemCreateSerializer, 
    OrderItemUpdateSerializer,
    OrderItemListSerializer
)
from orders.models import Order
from motopart.models import Motopart

class OrderItemListView(generics.ListCreateAPIView):
    """Get all order items or create a new order item"""
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see order items from their own orders
        return OrderItem.objects.filter(order__user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderItemCreateSerializer
        return OrderItemSerializer

class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a specific order item"""
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only access order items from their own orders
        return OrderItem.objects.filter(order__user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return OrderItemUpdateSerializer
        return OrderItemSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_items_by_order(request, order_id):
    """Get all items for a specific order"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)
        serializer = OrderItemListSerializer(order_items, many=True)
        return Response({
            'order_id': order.id,
            'order_status': order.status,
            'order_total': order.total_amount,
            'items': serializer.data,
            'items_count': order_items.count()
        })
    except Order.DoesNotExist:
        return Response(
            {'error': 'Order not found or access denied'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item_to_order(request, order_id):
    """Add an item to an existing order"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        
        # Get motopart and validate
        motopart_id = request.data.get('motopart')
        if not motopart_id:
            return Response(
                {'error': 'Motopart ID is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            motopart = Motopart.objects.get(id=motopart_id)
        except Motopart.DoesNotExist:
            return Response(
                {'error': 'Motopart not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if item already exists in order
        existing_item = OrderItem.objects.filter(order=order, motopart=motopart).first()
        if existing_item:
            # Update quantity
            quantity = request.data.get('quantity', 1)
            existing_item.quantity += quantity
            existing_item.save()
            serializer = OrderItemSerializer(existing_item)
            return Response({
                'message': 'Item quantity updated',
                'order_item': serializer.data
            }, status=status.HTTP_200_OK)
        
        # Create new order item
        order_item_data = {
            'order': order.id,
            'motopart': motopart.id,
            'quantity': request.data.get('quantity', 1),
            'unit_price': motopart.price
        }
        
        serializer = OrderItemCreateSerializer(data=order_item_data)
        if serializer.is_valid():
            order_item = serializer.save()
            response_serializer = OrderItemSerializer(order_item)
            return Response({
                'message': 'Item added to order successfully',
                'order_item': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Order.DoesNotExist:
        return Response(
            {'error': 'Order not found or access denied'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_item_quantity(request, order_item_id):
    """Update quantity of an order item"""
    try:
        order_item = OrderItem.objects.get(
            id=order_item_id, 
            order__user=request.user
        )
        
        quantity = request.data.get('quantity')
        if not quantity or quantity <= 0:
            return Response(
                {'error': 'Valid quantity is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order_item.quantity = quantity
        order_item.save()
        
        serializer = OrderItemSerializer(order_item)
        return Response({
            'message': 'Order item quantity updated',
            'order_item': serializer.data
        })
        
    except OrderItem.DoesNotExist:
        return Response(
            {'error': 'Order item not found or access denied'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_item_from_order(request, order_item_id):
    """Remove an item from an order"""
    try:
        order_item = OrderItem.objects.get(
            id=order_item_id, 
            order__user=request.user
        )
        order_item.delete()
        
        return Response({
            'message': 'Item removed from order successfully'
        }, status=status.HTTP_200_OK)
        
    except OrderItem.DoesNotExist:
        return Response(
            {'error': 'Order item not found or access denied'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_order_items(request, order_id):
    """Remove all items from an order"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_items = OrderItem.objects.filter(order=order)
        items_count = order_items.count()
        order_items.delete()
        
        return Response({
            'message': f'All items ({items_count}) removed from order successfully'
        }, status=status.HTTP_200_OK)
        
    except Order.DoesNotExist:
        return Response(
            {'error': 'Order not found or access denied'}, 
            status=status.HTTP_404_NOT_FOUND
        )
