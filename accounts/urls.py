from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]

api_urlpatterns = [
    path('auth/register/', views.RegisterAPIView.as_view(), name='api-register'),
    path('auth/login/', views.LoginAPIView.as_view(), name='api-login'),
    path('auth/logout/', views.LogoutAPIView.as_view(), name='api-logout'),
    path('auth/me/', views.MeAPIView.as_view(), name='api-me'),
]
