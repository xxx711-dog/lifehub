"""accounts serializers"""

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "username",
            "email",
            "date_joined",
            "avatar_color",
            "nickname",
            "city",
            "bio",
            "height",
            "weight",
            "diet_preference",
            "allergy",
            "monthly_budget",
            "commute_mode",
            "commute_minutes",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    nickname = serializers.CharField(write_only=True, required=False, default="")

    class Meta:
        model = User
        fields = ["username", "password", "email", "nickname"]

    def create(self, validated_data):
        nickname = validated_data.pop("nickname", "")
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email", ""),
        )
        UserProfile.objects.create(user=user, nickname=nickname or user.username)
        return user
