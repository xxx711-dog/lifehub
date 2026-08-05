"""travel urls"""

from django.urls import path
from .views import (
    TripListCreateView,
    TripDetailView,
    TripEventListCreateView,
    TripEventDetailView,
    PackingItemListCreateView,
    PackingItemDetailView,
    CommuteLogListCreateView,
    CommuteLogDetailView,
    CommuteSummaryView,
)

urlpatterns = [
    path("trips/", TripListCreateView.as_view(), name="trip-list"),
    path("trips/<int:pk>/", TripDetailView.as_view(), name="trip-detail"),
    path(
        "trips/<int:trip_pk>/events/",
        TripEventListCreateView.as_view(),
        name="event-list",
    ),
    path(
        "trips/<int:trip_pk>/events/<int:pk>/",
        TripEventDetailView.as_view(),
        name="event-detail",
    ),
    path(
        "trips/<int:trip_pk>/packing/",
        PackingItemListCreateView.as_view(),
        name="packing-list",
    ),
    path(
        "trips/<int:trip_pk>/packing/<int:pk>/",
        PackingItemDetailView.as_view(),
        name="packing-detail",
    ),
    path("commute/", CommuteLogListCreateView.as_view(), name="commute-list"),
    path("commute/<int:pk>/", CommuteLogDetailView.as_view(), name="commute-detail"),
    path("commute/summary/", CommuteSummaryView.as_view(), name="commute-summary"),
]
