from django.urls import path
from . import views

urlpatterns = [
    path('', views.MotopartListView.as_view(), name='motopart-list-create'),
]