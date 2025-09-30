from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartItemSerializer, CartItemCreateSerializer
from carts.models import Cart
from book.models import Book

# Create your views here.

class CartItemListView(generics.ListCreateAPIView):
    """Get cart items or add item to cart"""
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        cart_id = self.kwargs.get('cart_id')
        return CartItem.objects.filter(cart__id=cart_id, cart__user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartItemCreateSerializer
        return CartItemSerializer
    
    def perform_create(self, serializer):
        cart_id = self.kwargs.get('cart_id')
        cart = get_object_or_404(Cart, id=cart_id, user=self.request.user)
        
        # Check if item already exists in cart
        book_id = serializer.validated_data['book_id']
        existing_item = CartItem.objects.filter(cart=cart, book_id=book_id).first()
        
        if existing_item:
            # Update quantity instead of creating new item
            existing_item.quantity += serializer.validated_data['quantity']
            existing_item.save()
            return
        
        serializer.save(cart=cart)

class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a specific cart item"""
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        cart_id = self.kwargs.get('cart_id')
        return CartItem.objects.filter(
            cart__id=cart_id, 
            cart__user=self.request.user
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, cart_id):
    """Add item to cart"""
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    
    book_id = request.data.get('book_id')
    quantity = request.data.get('quantity', 1)
    
    if not book_id:
        return Response({
            'message': 'book_id is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({
            'message': 'Book not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check if item already exists in cart
    existing_item = CartItem.objects.filter(cart=cart, book=book).first()
    
    if existing_item:
        existing_item.quantity += quantity
        existing_item.save()
        serializer = CartItemSerializer(existing_item)
        return Response({
            'message': 'Item quantity updated in cart',
            'item': serializer.data
        }, status=status.HTTP_200_OK)
    else:
        cart_item = CartItem.objects.create(
            cart=cart,
            book=book,
            quantity=quantity
        )
        serializer = CartItemSerializer(cart_item)
        return Response({
            'message': 'Item added to cart',
            'item': serializer.data
        }, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item_quantity(request, cart_id, item_id):
    """Update quantity of a cart item"""
    cart_item = get_object_or_404(
        CartItem, 
        id=item_id, 
        cart__id=cart_id, 
        cart__user=request.user
    )
    
    quantity = request.data.get('quantity')
    if quantity is None:
        return Response({
            'message': 'quantity is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if quantity <= 0:
        cart_item.delete()
        return Response({
            'message': 'Item removed from cart'
        }, status=status.HTTP_200_OK)
    
    cart_item.quantity = quantity
    cart_item.save()
    
    serializer = CartItemSerializer(cart_item)
    return Response({
        'message': 'Item quantity updated',
        'item': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, cart_id, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(
        CartItem, 
        id=item_id, 
        cart__id=cart_id, 
        cart__user=request.user
    )
    
    cart_item.delete()
    return Response({
        'message': 'Item removed from cart'
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request, cart_id):
    """Clear all items from cart"""
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    CartItem.objects.filter(cart=cart).delete()
    
    return Response({
        'message': 'Cart cleared successfully'
    }, status=status.HTTP_200_OK)