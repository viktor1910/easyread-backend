from rest_framework import serializers
from .models import Order
from user.serializers import UserReadSerializer
from orderitem.serializers import OrderItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    user = UserReadSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(source='total_amount', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'status', 'total_amount', 'total_price', 'shipping_address',
            'billing_address', 'notes', 'created_at', 'updated_at', 'items'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'total_price', 'items']


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
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user_email', 'status', 'total_amount', 'created_at'
        ]


