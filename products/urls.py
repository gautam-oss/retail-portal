from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product-list'),
    path('<int:pk>/', views.product_detail, name='product-detail'),
    path('create/', views.product_create, name='product-create'),
    path('<int:pk>/edit/', views.product_update, name='product-update'),
    path('<int:pk>/delete/', views.product_delete, name='product-delete'),
    path('<int:pk>/stock/', views.stock_update, name='stock-update'),
]
