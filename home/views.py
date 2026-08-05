"""home views"""

from django.db.models import Sum, Q
from django.utils import timezone
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Expense, HouseTask, HomeInventory
from .serializers import ExpenseSerializer, HouseTaskSerializer, HomeInventorySerializer


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        qs = Expense.objects.filter(user=self.request.user)
        category = self.request.query_params.get("category")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        if category:
            qs = qs.filter(category=category)
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


class ExpenseSummaryView(APIView):
    """月度/区间消费统计"""

    def get(self, request):
        user = request.user
        today = timezone.now().date()
        month_start = today.replace(day=1)

        start = request.query_params.get("start_date", str(month_start))
        end = request.query_params.get("end_date", str(today))

        qs = Expense.objects.filter(user=user, date__gte=start, date__lte=end)
        total = qs.aggregate(total=Sum("amount"))["total"] or 0

        by_category = {}
        for item in (
            qs.values("category").annotate(total=Sum("amount")).order_by("-total")
        ):
            by_category[item["category"]] = float(item["total"])

        by_date = {}
        for item in qs.values("date").annotate(total=Sum("amount")).order_by("date"):
            by_date[str(item["date"])] = float(item["total"])

        return Response(
            {
                "start_date": start,
                "end_date": end,
                "total": float(total),
                "by_category": by_category,
                "by_date": by_date,
                "count": qs.count(),
            }
        )


class HouseTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = HouseTaskSerializer

    def get_queryset(self):
        qs = HouseTask.objects.filter(user=self.request.user)
        done = self.request.query_params.get("done")
        if done is not None:
            qs = qs.filter(is_done=done == "true")
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HouseTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HouseTaskSerializer

    def get_queryset(self):
        return HouseTask.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        # 完成周期性任务后，自动计算下次到期日
        if instance.is_done and instance.is_recurring and instance.interval_days:
            from datetime import timedelta

            instance.last_done_date = timezone.now().date()
            instance.next_due_date = timezone.now().date() + timedelta(
                days=instance.interval_days
            )
            instance.is_done = False
            instance.save()


class HomeInventoryListCreateView(generics.ListCreateAPIView):
    serializer_class = HomeInventorySerializer

    def get_queryset(self):
        qs = HomeInventory.objects.filter(user=self.request.user)
        low_stock = self.request.query_params.get("low_stock")
        if low_stock == "true":
            qs = qs.extra(where=["quantity <= min_quantity"])
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HomeInventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HomeInventorySerializer

    def get_queryset(self):
        return HomeInventory.objects.filter(user=self.request.user)
