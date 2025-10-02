from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('me/', views.get_user_orders, name='order-user-list'),
    path('admin/', views.OrderListAdminView.as_view(), name='order-admin-list'),
    path('<int:order_id>/status/', views.update_order_status, name='order-status-update'),
]
