from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Todo


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user info."""

    class Meta:
        model = User
        fields = ["id", "username", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration with password confirmation."""
    password = serializers.CharField(write_only=True, min_length=8, help_text="User password (min 8 chars)")

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
        return user


class TodoSerializer(serializers.ModelSerializer):
    """Serializer for Todo items with owner attribution."""
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Todo
        fields = [
            "id",
            "owner",
            "title",
            "description",
            "is_completed",
            "due_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]
