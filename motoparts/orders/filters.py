import django_filters
from .models import Order


class OrderAdminFilter(django_filters.FilterSet):
    """Custom filter for admin order list that supports multiple status values"""
    status = django_filters.MultipleChoiceFilter(
        field_name='status',
        choices=Order.STATUS_CHOICES,
        lookup_expr='in'
    )

    class Meta:
        model = Order
        fields = {
            'status': ['exact', 'in'],
            'user': ['exact'],
            'created_at': ['exact', 'gte', 'lte'],
        }
