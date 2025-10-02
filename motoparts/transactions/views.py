from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import Transaction
from .serializers import (
    TransactionSerializer, TransactionCreateSerializer, TransactionUpdateSerializer,
    TransactionStatusUpdateSerializer, TransactionListSerializer
)
from user.permissions import IsAdminUser

# Create your views here.

class TransactionListView(generics.ListCreateAPIView):
    """Get user's transactions or create a new transaction"""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own transactions
        # Admins can see all transactions
        if self.request.user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TransactionCreateSerializer
        return TransactionSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a specific transaction"""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only access their own transactions
        # Admins can access all transactions
        if self.request.user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=self.request.user)

class TransactionListAdminView(generics.ListAPIView):
    """Get all transactions - Admin only"""
    serializer_class = TransactionListSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return Transaction.objects.all()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_transactions(request):
    """Get all transactions for the current user"""
    transactions = Transaction.objects.filter(user=request.user)
    serializer = TransactionListSerializer(transactions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transaction_by_id(request, transaction_id):
    """Get transaction by transaction_id"""
    try:
        if request.user.is_staff:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
        else:
            transaction = Transaction.objects.get(
                transaction_id=transaction_id, 
                user=request.user
            )
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
    except Transaction.DoesNotExist:
        return Response({
            'message': 'Transaction not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction(request):
    """Create a new transaction"""
    serializer = TransactionCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        transaction = serializer.save()
        response_serializer = TransactionSerializer(transaction)
        return Response({
            'message': 'Transaction created successfully',
            'transaction': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'message': 'Transaction creation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_transaction_status(request, transaction_id):
    """Update transaction status"""
    try:
        if request.user.is_staff:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
        else:
            transaction = Transaction.objects.get(
                transaction_id=transaction_id, 
                user=request.user
            )
    except Transaction.DoesNotExist:
        return Response({
            'message': 'Transaction not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TransactionStatusUpdateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.update(transaction, serializer.validated_data)
        response_serializer = TransactionSerializer(transaction)
        return Response({
            'message': 'Transaction status updated successfully',
            'transaction': response_serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'message': 'Status update failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transaction_stats(request):
    """Get transaction statistics for user"""
    user_transactions = Transaction.objects.filter(user=request.user)
    
    stats = {
        'total_transactions': user_transactions.count(),
        'total_amount': sum(t.amount for t in user_transactions if t.is_successful),
        'pending_transactions': user_transactions.filter(status='pending').count(),
        'completed_transactions': user_transactions.filter(status='completed').count(),
        'failed_transactions': user_transactions.filter(status='failed').count(),
        'cancelled_transactions': user_transactions.filter(status='cancelled').count(),
        'refunded_transactions': user_transactions.filter(status='refunded').count(),
    }
    
    return Response(stats)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_admin_transaction_stats(request):
    """Get transaction statistics for admin"""
    all_transactions = Transaction.objects.all()
    
    stats = {
        'total_transactions': all_transactions.count(),
        'total_amount': sum(t.amount for t in all_transactions if t.is_successful),
        'pending_transactions': all_transactions.filter(status='pending').count(),
        'completed_transactions': all_transactions.filter(status='completed').count(),
        'failed_transactions': all_transactions.filter(status='failed').count(),
        'cancelled_transactions': all_transactions.filter(status='cancelled').count(),
        'refunded_transactions': all_transactions.filter(status='refunded').count(),
        'transactions_by_payment_method': {},
        'transactions_by_gateway': {},
    }
    
    # Payment method breakdown
    for method, _ in Transaction.PAYMENT_METHOD_CHOICES:
        stats['transactions_by_payment_method'][method] = all_transactions.filter(
            payment_method=method
        ).count()
    
    # Gateway breakdown
    for gateway, _ in Transaction.PAYMENT_GATEWAY_CHOICES:
        stats['transactions_by_gateway'][gateway] = all_transactions.filter(
            payment_gateway=gateway
        ).count()
    
    return Response(stats)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_transactions(request):
    """Search transactions with filters"""
    queryset = Transaction.objects.filter(user=request.user)
    
    # Apply filters
    status_filter = request.GET.get('status')
    payment_method_filter = request.GET.get('payment_method')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    amount_min = request.GET.get('amount_min')
    amount_max = request.GET.get('amount_max')
    
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    if payment_method_filter:
        queryset = queryset.filter(payment_method=payment_method_filter)
    
    if date_from:
        queryset = queryset.filter(created_at__gte=date_from)
    
    if date_to:
        queryset = queryset.filter(created_at__lte=date_to)
    
    if amount_min:
        queryset = queryset.filter(amount__gte=amount_min)
    
    if amount_max:
        queryset = queryset.filter(amount__lte=amount_max)
    
    serializer = TransactionListSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_payment(request):
    """Process payment for a transaction"""
    transaction_id = request.data.get('transaction_id')
    payment_data = request.data.get('payment_data', {})
    
    try:
        transaction = Transaction.objects.get(
            transaction_id=transaction_id, 
            user=request.user
        )
    except Transaction.DoesNotExist:
        return Response({
            'message': 'Transaction not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if transaction.status != 'pending':
        return Response({
            'message': f'Transaction is already {transaction.status}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Simulate payment processing
    # In real implementation, integrate with payment gateway
    try:
        # Mock payment processing
        transaction.external_transaction_id = f"ext_{transaction.transaction_id}"
        transaction.payment_reference = payment_data.get('reference', '')
        transaction.gateway_response = {
            'status': 'success',
            'gateway_transaction_id': transaction.external_transaction_id,
            'processed_at': str(transaction.updated_at)
        }
        transaction.mark_as_completed()
        
        serializer = TransactionSerializer(transaction)
        return Response({
            'message': 'Payment processed successfully',
            'transaction': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        transaction.mark_as_failed(str(e))
        return Response({
            'message': 'Payment processing failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)