from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import User, Admin, Role, AdminRole
from django.contrib.auth import authenticate

# ================= USER =================
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'mobile_phone', 'name', 'role']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            mobile_phone=validated_data.get('mobile_phone', ''),
            name=validated_data.get('name', ''),
            role=validated_data.get('role')
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['role'] = user.role.role_name if hasattr(user, 'role') else None
        return token

class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.role_name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'mobile_phone', 'role', 'role_name']

# ================= ADMIN =================
class AdminRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Admin
        fields = ['username', 'email', 'password', 'name', 'admin_role']
    
    def create(self, validated_data):
        admin = Admin.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            admin_role=validated_data.get('admin_role')
        )
        return admin

class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Debugging
        print("Received data:", attrs)
        
        authenticate_kwargs = {
            'username': attrs.get(self.username_field),
            'password': attrs.get('password'),
            'backend': 'core.backends.UserAuthBackend'
        }
        
        try:
            user = authenticate(**authenticate_kwargs)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            
            refresh = self.get_token(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        except Exception as e:
            print("Auth error:", str(e))
            raise serializers.ValidationError(str(e))

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Gunakan auth default untuk admin
        user = authenticate(
            username=attrs['username'],
            password=attrs['password']
        )
        
        if not user or not hasattr(user, 'admin_role'):
            raise serializers.ValidationError("Invalid admin credentials")
        
        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_type': 'admin'
        }
        return data

class AdminSerializer(serializers.ModelSerializer):
    admin_role_name = serializers.CharField(source='admin_role.admin_role_name', read_only=True)
    
    class Meta:
        model = Admin
        fields = ['id', 'username', 'email', 'name', 'admin_role', 'admin_role_name']