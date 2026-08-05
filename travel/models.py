"""行 - 出行管理模块

核心功能：
- 行程规划（旅行/出差计划 + 时间线）
- 通勤记录（每日通勤方式 + 时间）
- 出行清单（打包清单模板）
"""

from django.contrib.auth.models import User
from django.db import models


class TripStatus(models.TextChoices):
    PLANNED = "planned", "计划中"
    ONGOING = "ongoing", "进行中"
    COMPLETED = "completed", "已完成"
    CANCELLED = "cancelled", "已取消"


class Trip(models.Model):
    """行程 - 旅行/出差"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trips")
    title = models.CharField("行程名称", max_length=200)
    destination = models.CharField("目的地", max_length=200)
    start_date = models.DateField("出发日期")
    end_date = models.DateField("返回日期")
    trip_type = models.CharField(
        "类型", max_length=20, default="travel", help_text="travel=旅行, business=出差"
    )
    status = models.CharField(
        "状态", max_length=20, choices=TripStatus.choices, default=TripStatus.PLANNED
    )
    budget = models.DecimalField(
        "预算", max_digits=10, decimal_places=2, null=True, blank=True
    )
    actual_cost = models.DecimalField(
        "实际花费", max_digits=10, decimal_places=2, null=True, blank=True
    )
    transport = models.CharField(
        "交通方式",
        max_length=50,
        blank=True,
        default="",
        help_text="如：飞机、高铁、自驾",
    )
    accommodation = models.CharField("住宿", max_length=200, blank=True, default="")
    companions = models.CharField("同行人", max_length=200, blank=True, default="")
    notes = models.TextField("备注", blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "行程"
        verbose_name_plural = verbose_name
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.title} ({self.destination})"

    @property
    def duration_days(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0


class TripEvent(models.Model):
    """行程中的具体事件/安排 - 时间线"""

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="events")
    title = models.CharField("事件名称", max_length=200)
    date = models.DateField("日期")
    start_time = models.TimeField("开始时间", null=True, blank=True)
    end_time = models.TimeField("结束时间", null=True, blank=True)
    location = models.CharField("地点", max_length=200, blank=True, default="")
    category = models.CharField(
        "类别",
        max_length=30,
        default="activity",
        help_text="如：交通、景点、餐饮、住宿、购物",
    )
    cost = models.DecimalField(
        "花费", max_digits=8, decimal_places=2, null=True, blank=True
    )
    notes = models.TextField("备注", blank=True, default="")
    order = models.IntegerField("排序", default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "行程事件"
        verbose_name_plural = verbose_name
        ordering = ["date", "order", "start_time"]

    def __str__(self):
        return f"{self.trip.title} - {self.title}"


class CommuteLog(models.Model):
    """通勤记录 - 追踪每日出行方式与时间"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commute_logs"
    )
    date = models.DateField("日期")
    mode = models.CharField(
        "出行方式", max_length=20, help_text="如：地铁、公交、自驾、骑行、步行、打车"
    )
    destination = models.CharField(
        "目的地", max_length=100, blank=True, default="", help_text="如：公司、学校"
    )
    duration_minutes = models.IntegerField("耗时(分钟)", null=True, blank=True)
    distance_km = models.DecimalField(
        "距离(km)", max_digits=6, decimal_places=2, null=True, blank=True
    )
    cost = models.DecimalField(
        "花费(元)", max_digits=8, decimal_places=2, null=True, blank=True
    )
    note = models.TextField("备注", blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "通勤记录"
        verbose_name_plural = verbose_name
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.username} {self.date} {self.mode}"


class PackingItem(models.Model):
    """出行打包清单"""

    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="packing_items"
    )
    name = models.CharField("物品名", max_length=100)
    category = models.CharField(
        "分类",
        max_length=30,
        default="general",
        help_text="如：衣物、洗护、电子、证件、药品",
    )
    quantity = models.IntegerField("数量", default=1)
    is_packed = models.BooleanField("已打包", default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "打包清单"
        verbose_name_plural = verbose_name
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} x{self.quantity}"
