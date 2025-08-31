from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()
ROLE_CHOICES = ["owner", "admin", "waiter", "cashier"]

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = [
            "id", "first_name", "last_name", "username", "email",
            "role", "contact_number", "is_active", "is_blocked", "password"
        ]
        read_only_fields = ["is_active", "is_blocked"]
        extra_kwargs = {
            "password": {"write_only": True, "required": False}
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class UserCreateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ["is_active", "is_blocked"]



