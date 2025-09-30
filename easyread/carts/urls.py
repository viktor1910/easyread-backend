from django.urls import path
from . import views

urlpatterns = [
    # Cart endpoints
    path('', views.CartListView.as_view(), name='cart-list-create'),
    path('active/', views.get_active_cart, name='get-active-cart'),
    path('create/', views.create_cart, name='create-cart'),
    path('<int:pk>/', views.CartDetailView.as_view(), name='cart-detail'),
    path('<int:cart_id>/checkout/', views.checkout_cart, name='checkout-cart'),
]