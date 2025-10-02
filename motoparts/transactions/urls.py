from django.urls import path
from . import views

urlpatterns = [
    # Transaction CRUD endpoints
    path('', views.TransactionListView.as_view(), name='transaction-list-create'),
    path('<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    
    # User transaction endpoints
    path('user/', views.get_user_transactions, name='user-transactions'),
    path('stats/', views.get_transaction_stats, name='transaction-stats'),
    path('search/', views.search_transactions, name='search-transactions'),
    
    # Transaction by ID endpoints
    path('by-id/<str:transaction_id>/', views.get_transaction_by_id, name='transaction-by-id'),
    path('by-id/<str:transaction_id>/status/', views.update_transaction_status, name='update-transaction-status'),
    
    # Payment processing
    path('process-payment/', views.process_payment, name='process-payment'),
    
    # Admin endpoints
    path('admin/all/', views.TransactionListAdminView.as_view(), name='admin-transaction-list'),
    path('admin/stats/', views.get_admin_transaction_stats, name='admin-transaction-stats'),
]