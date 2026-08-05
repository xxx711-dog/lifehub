"""food serializers"""

from rest_framework import serializers
from .models import Recipe, MealLog, ShoppingItem


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]


class MealLogSerializer(serializers.ModelSerializer):
    recipe_title = serializers.CharField(
        source="recipe.title", read_only=True, default=""
    )

    class Meta:
        model = MealLog
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class ShoppingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingItem
        fields = "__all__"
        read_only_fields = ["user", "created_at"]
