"""home serializers"""

from rest_framework import serializers
from .models import Expense, HouseTask, HomeInventory


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"
        read_only_fields = ["user", "created_at"]


class HouseTaskSerializer(serializers.ModelSerializer):
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = HouseTask
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]

    def get_is_overdue(self, obj):
        from django.utils import timezone

        if obj.next_due_date and not obj.is_done:
            return obj.next_due_date < timezone.now().date()
        return False


class HomeInventorySerializer(serializers.ModelSerializer):
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = HomeInventory
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]
