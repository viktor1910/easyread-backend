from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Order
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

    def get_queryset(self):
        return Order.objects.all()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    queryset = Order.objects.filter(user=request.user)
    serializer = OrderListSerializer(queryset, many=True)
    return Response(serializer.data)


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

