from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart
from .serializers import CartSerializer, CartCreateSerializer

# Create your views here.

class CartListView(generics.ListCreateAPIView):
    """Get user's carts or create a new cart"""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartCreateSerializer
        return CartSerializer
    
    def perform_create(self, serializer):
        # Check if user already has an active cart
        existing_cart = Cart.objects.filter(
            user=self.request.user, 
            status='active'
        ).first()
        
        if existing_cart:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({
                'message': 'User already has an active cart',
                'cart_id': existing_cart.id
            })
        
        serializer.save(user=self.request.user)

class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a specific cart"""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_active_cart(request):
    """Get user's active cart"""
    try:
        cart = Cart.objects.get(user=request.user, status='active')
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    except Cart.DoesNotExist:
        return Response({
            'message': 'No active cart found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_cart(request):
    """Create a new cart for user"""
    # Check if user already has an active cart
    existing_cart = Cart.objects.filter(
        user=request.user, 
        status='active'
    ).first()
    
    if existing_cart:
        return Response({
            'message': 'User already has an active cart',
            'cart_id': existing_cart.id
        }, status=status.HTTP_400_BAD_REQUEST)
    
    cart = Cart.objects.create(user=request.user, status='active')
    serializer = CartSerializer(cart)
    return Response({
        'message': 'Cart created successfully',
        'cart': serializer.data
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_cart(request, cart_id):
    """Checkout a cart (change status to checked_out)"""
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    
    if cart.status == 'checked_out':
        return Response({
            'message': 'Cart is already checked out'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    cart.status = 'checked_out'
    cart.save()
    
    serializer = CartSerializer(cart)
    return Response({
        'message': 'Cart checked out successfully',
        'cart': serializer.data
    }, status=status.HTTP_200_OK)