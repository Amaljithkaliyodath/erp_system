from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    login_page, 
    dashboard_page, 
    RegisterView, 
    UserListCreateDeleteUpdateView, 
    ProfileView
)

urlpatterns = [
    # Frontend Pages
    path('', login_page, name='login'),                 
    path('dashboard/', dashboard_page, name='dashboard'),

    # JWT Auth API
    path('api/login/', TokenObtainPairView.as_view(), name='api_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Register API (Admin adds users, or public signup if allowed)
    path('api/register/', RegisterView.as_view(), name='register'),

    # User APIs
    path('api/users/', UserListCreateDeleteUpdateView.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserListCreateDeleteUpdateView.as_view(), name='user-detail'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
]
