from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "nickname", "city", "diet_preference", "commute_mode"]
    list_filter = ["city"]
    search_fields = ["user__username", "nickname"]
