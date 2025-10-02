from django.urls import path
from . import views

urlpatterns = [
    # CartItem endpoints
    path('cart/<int:cart_id>/items/', views.CartItemListView.as_view(), name='cartitem-list-create'),
    path('cart/<int:cart_id>/items/<int:pk>/', views.CartItemDetailView.as_view(), name='cartitem-detail'),
    path('cart/<int:cart_id>/add/', views.add_to_cart, name='add-to-cart'),
    path('cart/<int:cart_id>/items/<int:item_id>/update/', views.update_cart_item_quantity, name='update-cart-item'),
    path('cart/<int:cart_id>/items/<int:item_id>/remove/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/<int:cart_id>/clear/', views.clear_cart, name='clear-cart'),
]