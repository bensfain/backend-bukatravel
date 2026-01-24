from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Admin
from .api.serializers import (
    UserRegisterSerializer, UserTokenObtainPairSerializer,
    UserSerializer, AdminRegisterSerializer, 
    AdminTokenObtainPairSerializer, AdminSerializer
)

# ================= USER AUTH =================
class UserRegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

class UserLoginView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        print(f"Login attempt for {request.data.get('username')}")
        return super().post(request, *args, **kwargs)

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

# ================= ADMIN AUTH =================
class AdminRegisterView(generics.CreateAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminRegisterSerializer

class AdminLoginView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

class AdminProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AdminSerializer
    
    def get_object(self):
        return self.request.user

# ================= PROTECTED VIEWS =================
class UserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]  # Hanya admin yang bisa akses
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RoleBasedDataView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Contoh: Filter data berdasarkan role
        if hasattr(user, 'role'):
            if user.role.role_name == "Corporate":
                return User.objects.filter(role__role_name="Corporate")
            elif user.role.role_name == "Regular":
                return User.objects.filter(role__role_name="Regular")
        
        return User.objects.none()
    
    serializer_class = UserSerializer

# ================= TOKEN REFRESH =================
class TokenRefreshView(generics.GenericAPIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )