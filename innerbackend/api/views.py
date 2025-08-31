from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, serializers
from .serializers import UserSerializer, UserCreateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsOwnerOrAdminForUserManagement
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "role": getattr(request.user, "role", "user"),  # assuming User has a role field
        })
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdminForUserManagement]

    def get_serializer_class(self):
        return UserCreateSerializer if self.action == "create" else UserSerializer

    def perform_create(self, serializer):
        creator = self.request.user
        role_to_create = self.request.data.get("role")

        if getattr(creator, "role", None) == "owner":
            serializer.save()
        elif getattr(creator, "role", None) == "admin":
            if role_to_create not in ("waiter", "cashier"):
                raise serializers.ValidationError("Admins can only create waiter or cashier accounts.")
            serializer.save()
        else:
            raise serializers.ValidationError("Not allowed.")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def block(self, request, pk=None):
        user = self.get_object()
        self.check_object_permissions(request, user)
        user.is_blocked = True
        user.save()
        return Response({"status": "blocked"})

    @action(detail=True, methods=["post"])
    def unblock(self, request, pk=None):
        user = self.get_object()
        self.check_object_permissions(request, user)
        user.is_blocked = False
        user.save()
        return Response({"status": "unblocked"})

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Call the default validation first (checks username/password)
        data = super().validate(attrs)

        # Check if the user is blocked
        if self.user.is_blocked:
            raise serializers.ValidationError({"code": "blocked", "message": "This account is blocked."})
        return data
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer