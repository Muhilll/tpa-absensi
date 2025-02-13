from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from admintpa.models import User

class CustomUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            # Periksa password yang sudah di-hash dengan method bawaan
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
