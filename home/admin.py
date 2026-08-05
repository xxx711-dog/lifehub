from django.contrib import admin
from .models import Expense, HouseTask, HomeInventory


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "amount", "category", "date", "payment_method"]
    list_filter = ["category", "date", "payment_method"]
    search_fields = ["title", "store"]


@admin.register(HouseTask)
class HouseTaskAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "is_recurring",
        "frequency",
        "next_due_date",
        "is_done",
        "priority",
    ]
    list_filter = ["is_recurring", "is_done", "priority"]
    search_fields = ["title"]


@admin.register(HomeInventory)
class HomeInventoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "quantity", "unit", "min_quantity", "location"]
    list_filter = ["category", "location"]
    search_fields = ["name"]
