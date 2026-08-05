from django.contrib import admin
from .models import Recipe, MealLog, ShoppingItem


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "cuisine",
        "difficulty",
        "cook_time",
        "is_public",
    ]
    list_filter = ["category", "cuisine", "is_public"]
    search_fields = ["title", "tags", "ingredients"]


@admin.register(MealLog)
class MealLogAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "date",
        "meal_type",
        "recipe",
        "custom_food",
        "calories",
        "cost",
    ]
    list_filter = ["meal_type", "date"]
    search_fields = ["user__username", "custom_food"]


@admin.register(ShoppingItem)
class ShoppingItemAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "quantity",
        "category",
        "is_purchased",
        "estimated_price",
        "actual_price",
    ]
    list_filter = ["category", "is_purchased"]
    search_fields = ["name", "store"]
