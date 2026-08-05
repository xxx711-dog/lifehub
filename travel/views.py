"""travel views"""

from django.db.models import Q, Sum, Count
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Trip, TripEvent, CommuteLog, PackingItem
from .serializers import (
    TripSerializer,
    TripEventSerializer,
    CommuteLogSerializer,
    PackingItemSerializer,
)


class TripListCreateView(generics.ListCreateAPIView):
    serializer_class = TripSerializer

    def get_queryset(self):
        qs = Trip.objects.filter(user=self.request.user)
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TripSerializer

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)


class TripEventListCreateView(generics.ListCreateAPIView):
    serializer_class = TripEventSerializer

    def get_queryset(self):
        return TripEvent.objects.filter(trip_id=self.kwargs["trip_pk"]).order_by(
            "date", "order"
        )

    def perform_create(self, serializer):
        trip = Trip.objects.get(id=self.kwargs["trip_pk"], user=self.request.user)
        serializer.save(trip=trip)


class TripEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TripEventSerializer

    def get_queryset(self):
        return TripEvent.objects.filter(trip__user=self.request.user)


class PackingItemListCreateView(generics.ListCreateAPIView):
    serializer_class = PackingItemSerializer

    def get_queryset(self):
        return PackingItem.objects.filter(trip_id=self.kwargs["trip_pk"])

    def perform_create(self, serializer):
        trip = Trip.objects.get(id=self.kwargs["trip_pk"], user=self.request.user)
        serializer.save(trip=trip)


class PackingItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PackingItemSerializer

    def get_queryset(self):
        return PackingItem.objects.filter(trip__user=self.request.user)


class CommuteLogListCreateView(generics.ListCreateAPIView):
    serializer_class = CommuteLogSerializer

    def get_queryset(self):
        qs = CommuteLog.objects.filter(user=self.request.user)
        date = self.request.query_params.get("date")
        if date:
            qs = qs.filter(date=date)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommuteLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommuteLogSerializer

    def get_queryset(self):
        return CommuteLog.objects.filter(user=self.request.user)


class CommuteSummaryView(APIView):
    """通勤统计"""

    def get(self, request):
        user = request.user
        from django.utils import timezone
        from datetime import timedelta

        today = timezone.now().date()
        week_ago = today - timedelta(days=7)

        qs = CommuteLog.objects.filter(user=user, date__gte=week_ago)
        total_cost = qs.aggregate(total=Sum("cost"))["total"] or 0
        avg_duration = qs.aggregate(avg=Sum("duration_minutes"))["avg"]

        by_mode = {}
        for item in qs.values("mode").annotate(count=Count("id")):
            by_mode[item["mode"]] = item["count"]

        return Response(
            {
                "week_start": str(week_ago),
                "week_end": str(today),
                "total_trips": qs.count(),
                "total_cost": float(total_cost),
                "avg_duration": avg_duration / qs.count()
                if qs.count() and avg_duration
                else 0,
                "by_mode": by_mode,
            }
        )
