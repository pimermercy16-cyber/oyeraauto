from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('visits/', views.visit_list, name='visit_list'),
    path('visits/new/', views.create_visit, name='create_visit'),
    path('visits/<int:pk>/', views.visit_detail, name='visit_detail'),
]
