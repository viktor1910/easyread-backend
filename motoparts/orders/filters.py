import django_filters
from .models import Order


class OrderFilter(django_filters.FilterSet):
    """Custom filter for Order model to support multiple status values"""
    status = django_filters.MultipleChoiceFilter(
        field_name='status',
        choices=Order.STATUS_CHOICES
    )

    class Meta:
        model = Order
        fields = ['status', 'user', 'created_at']
