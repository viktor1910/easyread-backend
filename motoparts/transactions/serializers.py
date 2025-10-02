from rest_framework import serializers
from .models import Transaction
from user.serializers import UserReadSerializer

class TransactionSerializer(serializers.ModelSerializer):
    user = UserReadSerializer(read_only=True)
    is_successful = serializers.ReadOnlyField()
    is_pending = serializers.ReadOnlyField()
    is_failed = serializers.ReadOnlyField()
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'order', 'transaction_id', 'external_transaction_id',
            'amount', 'currency', 'status', 'payment_method', 'payment_gateway',
            'payment_reference', 'gateway_response', 'created_at', 'updated_at',
            'completed_at', 'description', 'notes', 'is_successful', 'is_pending', 'is_failed'
        ]
        read_only_fields = [
            'id', 'user', 'transaction_id', 'created_at', 'updated_at',
            'completed_at', 'is_successful', 'is_pending', 'is_failed'
        ]

class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'order', 'amount', 'currency', 'payment_method', 'payment_gateway',
            'payment_reference', 'description', 'notes'
        ]
        
    def create(self, validated_data):
        # Automatically assign the current user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
        
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value

class TransactionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'status', 'external_transaction_id', 'payment_reference',
            'gateway_response', 'description', 'notes'
        ]
        
    def validate_status(self, value):
        # Prevent invalid status transitions
        instance = self.instance
        if instance:
            current_status = instance.status
            
            # Define valid transitions
            valid_transitions = {
                'pending': ['completed', 'failed', 'cancelled'],
                'completed': ['refunded'],
                'failed': ['pending'],  # Allow retry
                'cancelled': ['pending'],  # Allow retry
                'refunded': []  # No transitions from refunded
            }
            
            if value not in valid_transitions.get(current_status, []):
                raise serializers.ValidationError(
                    f"Cannot change status from {current_status} to {value}"
                )
        
        return value

class TransactionStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Transaction.STATUS_CHOICES)
    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def update(self, instance, validated_data):
        status = validated_data['status']
        reason = validated_data.get('reason', '')
        
        if status == 'completed':
            instance.mark_as_completed()
        elif status == 'failed':
            instance.mark_as_failed(reason)
        elif status == 'cancelled':
            instance.mark_as_cancelled(reason)
        elif status == 'refunded':
            instance.mark_as_refunded(reason)
        else:
            instance.status = status
            if reason:
                instance.notes = reason
            instance.save()
            
        return instance

class TransactionListSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    order_id = serializers.IntegerField(source='order.id', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_id', 'user_email', 'order_id', 'amount', 'currency',
            'status', 'payment_method', 'created_at', 'completed_at'
        ]
