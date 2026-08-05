"""food urls"""

from django.urls import path
from .views import (
    RecipeListCreateView,
    RecipeDetailView,
    MealLogListCreateView,
    MealLogDetailView,
    ShoppingItemListCreateView,
    ShoppingItemDetailView,
    FoodSuggestView,
)

urlpatterns = [
    path("recipes/", RecipeListCreateView.as_view(), name="recipe-list"),
    path("recipes/<int:pk>/", RecipeDetailView.as_view(), name="recipe-detail"),
    path("meals/", MealLogListCreateView.as_view(), name="meal-list"),
    path("meals/<int:pk>/", MealLogDetailView.as_view(), name="meal-detail"),
    path("shopping/", ShoppingItemListCreateView.as_view(), name="shopping-list"),
    path(
        "shopping/<int:pk>/", ShoppingItemDetailView.as_view(), name="shopping-detail"
    ),
    path("suggest/", FoodSuggestView.as_view(), name="food-suggest"),
]
