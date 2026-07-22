from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('customers/new/', views.create_customer, name='create_customer'),
    path('vehicles/new/', views.create_vehicle, name='create_vehicle'),
    path('visits/', views.visit_list, name='visit_list'),
    path('visits/new/', views.create_visit, name='create_visit'),
    path('visits/<int:pk>/', views.visit_detail, name='visit_detail'),
    path('inventory/', views.part_list, name='part_list'),
    path('inventory/new/', views.create_part, name='create_part'),
]