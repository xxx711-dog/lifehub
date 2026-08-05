"""accounts views - 注册、档案、仪表盘聚合"""

from datetime import timedelta
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import UserProfileSerializer, RegisterSerializer

from wardrobe.models import Clothing, OutfitLog
from food.models import Recipe, MealLog, ShoppingItem
from home.models import Expense, HouseTask, HomeInventory
from travel.models import Trip, CommuteLog


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class UserProfileView(APIView):
    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return Response(UserProfileSerializer(profile).data)

    def put(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PasswordChangeView(APIView):
    def post(self, request):
        user = request.user
        old = request.data.get("old_password", "")
        new = request.data.get("new_password", "")
        if not user.check_password(old):
            return Response({"error": "旧密码错误"}, status=400)
        if len(new) < 6:
            return Response({"error": "新密码至少6位"}, status=400)
        user.set_password(new)
        user.save()
        return Response({"message": "密码修改成功"})


class DashboardView(APIView):
    """仪表盘聚合 - 返回四模块概览数据"""

    def get(self, request):
        user = request.user
        today = timezone.now().date()
        month_start = today.replace(day=1)

        # 衣
        wardrobe_count = Clothing.objects.filter(user=user).count()
        today_outfit = OutfitLog.objects.filter(user=user, date=today).first()
        recent_outfits = OutfitLog.objects.filter(user=user).count()

        # 食
        today_meals = MealLog.objects.filter(user=user, date=today).count()
        recipe_count = Recipe.objects.filter(Q(user=user) | Q(is_public=True)).count()
        pending_shopping = ShoppingItem.objects.filter(
            user=user, is_purchased=False
        ).count()

        # 住
        month_expenses = Expense.objects.filter(user=user, date__gte=month_start)
        month_total = month_expenses.aggregate(total=Sum("amount"))["total"] or 0
        category_breakdown = {}
        for cat in month_expenses.values("category").annotate(total=Sum("amount")):
            category_breakdown[cat["category"]] = float(cat["total"])

        pending_tasks = HouseTask.objects.filter(user=user, is_done=False).count()
        overdue_tasks = HouseTask.objects.filter(
            user=user, is_done=False, next_due_date__lt=today
        ).count()
        low_stock = (
            HomeInventory.objects.filter(user=user)
            .extra(where=["quantity <= min_quantity"])
            .count()
        )

        # 行
        upcoming_trips = Trip.objects.filter(
            user=user, start_date__gte=today, status="planned"
        ).order_by("start_date")[:3]
        commute_this_week = CommuteLog.objects.filter(
            user=user, date__gte=today - timedelta(days=7)
        ).count()

        return Response(
            {
                "user": {
                    "username": user.username,
                    "nickname": getattr(user, "profile", None)
                    and user.profile.nickname
                    or user.username,
                },
                "wardrobe": {
                    "total_clothes": wardrobe_count,
                    "today_outfit_logged": bool(today_outfit),
                    "total_outfits": recent_outfits,
                },
                "food": {
                    "today_meals": today_meals,
                    "recipe_count": recipe_count,
                    "pending_shopping": pending_shopping,
                },
                "home": {
                    "month_expense": float(month_total),
                    "category_breakdown": category_breakdown,
                    "pending_tasks": pending_tasks,
                    "overdue_tasks": overdue_tasks,
                    "low_stock_items": low_stock,
                },
                "travel": {
                    "upcoming_trips": [
                        {
                            "id": t.id,
                            "title": t.title,
                            "destination": t.destination,
                            "start_date": str(t.start_date),
                            "end_date": str(t.end_date),
                            "days": t.duration_days,
                        }
                        for t in upcoming_trips
                    ],
                    "commute_this_week": commute_this_week,
                },
                "date": str(today),
            }
        )
