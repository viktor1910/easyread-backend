from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart
from django.db import transaction
from decimal import Decimal
from orders.models import Order
from orderitem.models import OrderItem
from orders.serializers import OrderSerializer
from transactions.models import Transaction
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
    """Checkout a cart: create Order and OrderItems, then mark cart as checked_out"""
    cart = get_object_or_404(Cart, id=cart_id, user=request.user)

    if cart.status == 'checked_out':
        return Response({
            'message': 'Cart is already checked out'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Extract checkout payload
    shipping_address = request.data.get('shipping_address', '')
    billing_address = request.data.get('billing_address', '')
    notes = request.data.get('notes', '')

    if not shipping_address:
        return Response({'message': 'shipping_address is required'}, status=status.HTTP_400_BAD_REQUEST)

    cart_items = list(cart.items.select_related('motopart').all())
    if not cart_items:
        return Response({'message': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        # Compute total from cart items (using discounted price)
        total_amount = Decimal('0.00')
        for item in cart_items:
            # item.total may be Decimal-compatible
            total_amount += Decimal(str(item.total))

        order = Order.objects.create(
            user=request.user,
            status='pending',
            total_amount=total_amount,
            shipping_address=shipping_address,
            billing_address=billing_address or None,
            notes=notes or None,
        )

        # Create order items
        for item in cart_items:
            unit_price = Decimal(str(item.unit_price))
            OrderItem.objects.create(
                order=order,
                motopart=item.motopart,
                quantity=item.quantity,
                unit_price=unit_price,
                total=unit_price * item.quantity,
            )

        # Optionally create a pending transaction for this order
        payment_method = request.data.get('payment_method')
        payment_gateway = request.data.get('payment_gateway', 'manual')
        currency = request.data.get('currency', 'USD')
        payment_reference = request.data.get('payment_reference')

        created_transaction = None
        if payment_method:
            created_transaction = Transaction.objects.create(
                user=request.user,
                order=order,
                amount=order.total_amount,
                currency=currency,
                status='pending',
                payment_method=payment_method,
                payment_gateway=payment_gateway,
                payment_reference=payment_reference or None,
                description='Auto-created at checkout'
            )

        # Mark cart as checked out and optionally clear items
        cart.status = 'checked_out'
        cart.save()
        # Optionally delete cart items to prevent reuse
        # cart.items.all().delete()

    order_data = OrderSerializer(order).data
    response_data = {
        'message': 'Checkout successful',
        'order': order_data
    }
    if created_transaction:
        response_data['transaction_id'] = created_transaction.transaction_id
        response_data['transaction_status'] = created_transaction.status
    return Response(response_data, status=status.HTTP_201_CREATED)