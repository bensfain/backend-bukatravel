from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegisterView, UserProfileView,
    AdminRegisterView, AdminLoginView, AdminProfileView,
    UserListView, RoleBasedDataView, TokenRefreshView,
    UserLoginView
)

urlpatterns = [
    # User Endpoints
    path('user/register/', UserRegisterView.as_view(), name='user-register'),
    path('user/login/', UserLoginView.as_view(), name='user-logintp'),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Admin Endpoints
    path('admin/register/', AdminRegisterView.as_view(), name='admin-register'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('admin/profile/', AdminProfileView.as_view(), name='admin-profile'),
    
    # Protected Endpoints
    path('admin/users/', UserListView.as_view(), name='user-list'),
    path('role-based-data/', RoleBasedDataView.as_view(), name='role-based-data'),
    
    # Token
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]