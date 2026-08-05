"""travel serializers"""

from rest_framework import serializers
from .models import Trip, TripEvent, CommuteLog, PackingItem


class TripEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripEvent
        fields = "__all__"
        read_only_fields = ["created_at"]


class PackingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingItem
        fields = "__all__"
        read_only_fields = ["created_at"]


class TripSerializer(serializers.ModelSerializer):
    events = TripEventSerializer(many=True, read_only=True)
    packing_items = PackingItemSerializer(many=True, read_only=True)
    duration_days = serializers.IntegerField(read_only=True)

    class Meta:
        model = Trip
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]


class CommuteLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommuteLog
        fields = "__all__"
        read_only_fields = ["user", "created_at"]
