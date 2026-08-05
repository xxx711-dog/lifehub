from django.contrib import admin
from .models import Clothing, OutfitLog


@admin.register(Clothing)
class ClothingAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "color",
        "brand",
        "season",
        "wear_count",
        "is_favorite",
    ]
    list_filter = ["category", "season", "is_favorite"]
    search_fields = ["name", "brand", "color"]


class ClothingInline(admin.TabularInline):
    model = OutfitLog.clothes.through
    extra = 0


@admin.register(OutfitLog)
class OutfitLogAdmin(admin.ModelAdmin):
    list_display = ["user", "date", "occasion", "weather", "mood"]
    list_filter = ["date", "occasion"]
    search_fields = ["user__username", "note"]
    inlines = [ClothingInline]
