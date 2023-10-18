from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super(UserSerializer, self).create(validated_data)

    class Meta:
        model = User
        exclude = (
            "groups", "user_permissions", "is_superuser",
            "last_login", "password_reset_token")
        extra_kwargs = {
            "password": {"write_only": True},
            "is_staff": {"write_only": True}
        }
