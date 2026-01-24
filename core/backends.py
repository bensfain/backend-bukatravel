# core/backends.py
from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db.models import Q

class UserAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # UserModel = get_user_model()
        try:
            # Cari user by username atau email
            user = User.objects.get(
                Q(username__iexact=username) | 
                Q(email__iexact=username))
            
            if user.check_password(password) and user.is_active:
                return user
        except User.DoesNotExist:
            return None
        except Exception as e:
            print(f"Auth error: {str(e)}")
            return None