from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from categories.views import CategoryViewSet
from products.views import ProductViewSet
from accounts.urls import api_urlpatterns
from orders.urls import api_urlpatterns as order_api_urlpatterns
from . import views

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='api-category')
router.register(r'products', ProductViewSet, basename='api-product')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('categories/', include('categories.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('search/', include('search.urls')),
    path('api/', include(router.urls)),
    path('api/', include(api_urlpatterns)),
    path('api/', include(order_api_urlpatterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
