from rest_framework import serializers
from .models import Order
from user.serializers import UserReadSerializer
from motopart.serializers import MotopartSerializer


class OrderItemDetailSerializer(serializers.Serializer):
    """Nested serializer for order items with motopart details"""
    id = serializers.IntegerField()
    motopart = MotopartSerializer()
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='unit_price')
    total = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderSerializer(serializers.ModelSerializer):
    user = UserReadSerializer(read_only=True)
    items = OrderItemDetailSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='total_amount', read_only=True)
    payment_method = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'status', 'total_amount', 'total_price', 'shipping_address',
            'billing_address', 'notes', 'payment_method', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_payment_method(self, obj):
        # Default to COD for now, can be enhanced later with actual payment tracking
        return 'cod'


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'total_amount', 'shipping_address', 'billing_address', 'notes'
        ]

    def validate_total_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Total amount must be greater than 0')
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'status', 'shipping_address', 'billing_address', 'notes'
        ]

    def validate_status(self, value):
        instance = self.instance
        if instance is None:
            return value

        current_status = instance.status
        valid_transitions = {
            'pending': ['confirmed', 'cancelled'],
            'confirmed': ['processing', 'cancelled'],
            'processing': ['shipped', 'cancelled'],
            'shipped': ['delivered'],
            'delivered': [],
            'cancelled': [],
            'refunded': [],
        }

        if value not in valid_transitions.get(current_status, []):
            raise serializers.ValidationError(
                f"Cannot change status from {current_status} to {value}"
            )
        return value


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)

    def update(self, instance, validated_data):
        status = validated_data['status']
        reason = validated_data.get('reason', '')

        # Use same validation as OrderUpdateSerializer
        serializer = OrderUpdateSerializer(instance, data={'status': status}, partial=True)
        serializer.is_valid(raise_exception=True)

        instance.status = status
        if reason:
            instance.notes = (instance.notes + '\n' if instance.notes else '') + reason
        instance.save()
        return instance


class OrderListSerializer(serializers.ModelSerializer):
    user = UserReadSerializer(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='total_amount', read_only=True)
    payment_method = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'status', 'total_amount', 'total_price', 'shipping_address',
            'payment_method', 'created_at', 'updated_at'
        ]

    def get_payment_method(self, obj):
        return 'cod'


