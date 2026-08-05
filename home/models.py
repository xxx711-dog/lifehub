"""住 - 家居生活管理模块

核心功能：
- 记账（日常开销分类统计 + 月度预算追踪）
- 家务待办（周期性家务提醒）
- 家居物品库存（消耗品管理 + 补货提醒）
"""

from django.contrib.auth.models import User
from django.db import models


class ExpenseCategory(models.TextChoices):
    FOOD = "food", "餐饮"
    RENT = "rent", "房租/房贷"
    UTILITY = "utility", "水电煤网"
    TRANSPORT = "transport", "交通"
    SHOPPING = "shopping", "购物"
    ENTERTAINMENT = "entertainment", "娱乐"
    MEDICAL = "medical", "医疗"
    EDUCATION = "education", "教育"
    OTHER = "other", "其他"


class Expense(models.Model):
    """记账记录"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField("金额", max_digits=10, decimal_places=2)
    category = models.CharField(
        "分类",
        max_length=20,
        choices=ExpenseCategory.choices,
        default=ExpenseCategory.OTHER,
    )
    title = models.CharField("名称", max_length=200)
    date = models.DateField("日期")
    payment_method = models.CharField(
        "支付方式",
        max_length=20,
        blank=True,
        default="",
        help_text="如：微信、支付宝、银行卡、现金",
    )
    store = models.CharField("商家", max_length=100, blank=True, default="")
    note = models.TextField("备注", blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "支出记录"
        verbose_name_plural = verbose_name
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.title} -{self.amount} ({self.get_category_display()})"


class HouseTask(models.Model):
    """家务待办 - 支持周期性提醒"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="house_tasks")
    title = models.CharField("家务名称", max_length=100)
    description = models.TextField("描述", blank=True, default="")

    # 周期：一次性 / 每天 / 每周 / 每月
    is_recurring = models.BooleanField("周期性", default=False)
    frequency = models.CharField(
        "频率",
        max_length=20,
        blank=True,
        default="",
        help_text="如：每天、每周一、每月1号",
    )
    interval_days = models.IntegerField(
        "间隔天数", null=True, blank=True, help_text="每隔几天执行一次"
    )

    next_due_date = models.DateField("下次到期日", null=True, blank=True)
    last_done_date = models.DateField("上次完成日", null=True, blank=True)
    is_done = models.BooleanField("本次已完成", default=False)
    priority = models.IntegerField("优先级(1-3)", default=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "家务待办"
        verbose_name_plural = verbose_name
        ordering = ["priority", "next_due_date"]

    def __str__(self):
        return self.title


class HomeInventory(models.Model):
    """家居物品库存 - 消耗品管理"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="inventory_items"
    )
    name = models.CharField("物品名", max_length=100)
    category = models.CharField(
        "分类", max_length=30, help_text="如：纸巾、洗护、清洁、厨房"
    )
    quantity = models.DecimalField("数量", max_digits=10, decimal_places=2, default=1)
    unit = models.CharField("单位", max_length=20, default="个")
    min_quantity = models.DecimalField(
        "最低库存", max_digits=10, decimal_places=2, default=1
    )
    location = models.CharField(
        "存放位置",
        max_length=50,
        blank=True,
        default="",
        help_text="如：厨房柜、卫生间、阳台",
    )
    purchase_date = models.DateField("购买日期", null=True, blank=True)
    expiry_date = models.DateField("过期日期", null=True, blank=True)
    price = models.DecimalField(
        "价格", max_digits=8, decimal_places=2, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "家居库存"
        verbose_name_plural = verbose_name
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} ({self.quantity}{self.unit})"

    @property
    def is_low_stock(self):
        return self.quantity <= self.min_quantity
