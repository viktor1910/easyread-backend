from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from .models import Order
from .pagination import OrderPagination, OrderAdminPagination
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderUpdateSerializer,
    OrderStatusUpdateSerializer,
    OrderListSerializer,
)
from user.permissions import IsAdminUser


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = OrderPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'user']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'shipping_address']
    ordering_fields = ['created_at', 'updated_at', 'total_amount', 'status']
    ordering = ['-created_at']  # Default ordering

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        create_serializer = self.get_serializer_class()
        serializer = create_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        full_serializer = OrderSerializer(order)
        headers = self.get_success_headers(full_serializer.data)
        return Response(full_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return OrderUpdateSerializer
        return OrderSerializer

    def perform_update(self, serializer):
        # Only admin can update status field
        if not self.request.user.is_staff and 'status' in self.request.data:
            raise PermissionDenied('Only admin can update order status')
        serializer.save()


class OrderListAdminView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAdminUser]
    pagination_class = OrderAdminPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'user', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'id', 'shipping_address']
    ordering_fields = ['created_at', 'updated_at', 'total_amount', 'status', 'user__email']
    ordering = ['-created_at']  # Default ordering

    def get_queryset(self):
        return Order.objects.all()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    """
    Get user's orders with pagination support
    This endpoint is deprecated - use OrderListCreateView instead
    """
    queryset = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Simple pagination for function-based view
    page_size = int(request.GET.get('page_size', 10))
    page = int(request.GET.get('page', 1))
    
    start = (page - 1) * page_size
    end = start + page_size
    
    total_count = queryset.count()
    orders = queryset[start:end]
    
    serializer = OrderListSerializer(orders, many=True)
    
    return Response({
        'pagination': {
            'count': total_count,
            'current_page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size,
        },
        'results': serializer.data
    })


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderStatusUpdateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.update(order, serializer.validated_data)
        response = OrderSerializer(order)
        return Response({'message': 'Order status updated successfully', 'order': response.data})

    return Response({'message': 'Status update failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

