from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order-list'),
    path('<int:pk>/', views.order_detail, name='order-detail'),
    path('create/', views.order_create, name='order-create'),
    path('<int:pk>/reorder/', views.order_reorder, name='order-reorder'),
]

api_urlpatterns = [
    path('orders/', views.OrderListCreateAPIView.as_view(), name='api-orders'),
    path('orders/<int:pk>/', views.OrderDetailAPIView.as_view(), name='api-order-detail'),
    path('orders/<int:pk>/reorder/', views.order_reorder_api, name='api-order-reorder'),
]
