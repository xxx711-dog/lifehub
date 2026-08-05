"""wardrobe urls"""

from django.urls import path
from .views import (
    ClothingListCreateView,
    ClothingDetailView,
    OutfitLogListCreateView,
    OutfitLogDetailView,
    WardrobeSuggestView,
)

urlpatterns = [
    path("clothes/", ClothingListCreateView.as_view(), name="clothing-list"),
    path("clothes/<int:pk>/", ClothingDetailView.as_view(), name="clothing-detail"),
    path("outfits/", OutfitLogListCreateView.as_view(), name="outfit-list"),
    path("outfits/<int:pk>/", OutfitLogDetailView.as_view(), name="outfit-detail"),
    path("suggest/", WardrobeSuggestView.as_view(), name="wardrobe-suggest"),
]
