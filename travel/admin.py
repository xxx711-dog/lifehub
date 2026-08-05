from django.contrib import admin
from .models import Trip, TripEvent, CommuteLog, PackingItem


class TripEventInline(admin.TabularInline):
    model = TripEvent
    extra = 0


class PackingItemInline(admin.TabularInline):
    model = PackingItem
    extra = 0


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "destination",
        "start_date",
        "end_date",
        "status",
        "trip_type",
    ]
    list_filter = ["status", "trip_type"]
    search_fields = ["title", "destination"]
    inlines = [TripEventInline, PackingItemInline]


@admin.register(CommuteLog)
class CommuteLogAdmin(admin.ModelAdmin):
    list_display = ["user", "date", "mode", "destination", "duration_minutes", "cost"]
    list_filter = ["mode", "date"]
    search_fields = ["user__username", "destination"]
