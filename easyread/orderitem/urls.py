from django.urls import path
from . import views

urlpatterns = [
    # Basic CRUD operations
    path('', views.OrderItemListView.as_view(), name='orderitem-list-create'),
    path('<int:pk>/', views.OrderItemDetailView.as_view(), name='orderitem-detail'),
    
    # Order-specific operations
    path('order/<int:order_id>/items/', views.get_order_items_by_order, name='order-items-by-order'),
    path('order/<int:order_id>/add/', views.add_item_to_order, name='add-item-to-order'),
    path('order/<int:order_id>/clear/', views.clear_order_items, name='clear-order-items'),
    
    # Item-specific operations
    path('<int:order_item_id>/update-quantity/', views.update_order_item_quantity, name='update-order-item-quantity'),
    path('<int:order_item_id>/remove/', views.remove_item_from_order, name='remove-item-from-order'),
]
