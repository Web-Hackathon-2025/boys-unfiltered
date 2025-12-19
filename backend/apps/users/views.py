from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer

# Simple view for user registration (we'll implement fully later)
class UserCreateView(generics.CreateAPIView):
    queryset = None
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]