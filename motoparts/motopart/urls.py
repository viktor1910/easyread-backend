from django.urls import path
from . import views

urlpatterns = [
    path('', views.MotopartListView.as_view(), name='motopart-list-create'),
    path('<int:pk>/', views.MotopartDetailView.as_view(), name='motopart-detail'),
]