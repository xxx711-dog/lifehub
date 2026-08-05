"""衣 - 衣橱管理模块

核心功能：
- 衣物管理（分类、季节、颜色、穿着记录）
- 穿搭日记（记录每日穿搭 + 天气 + 场合）
- 智能推荐（根据天气/场合/历史穿搭推荐搭配）
"""

from django.contrib.auth.models import User
from django.db import models


class Category(models.TextChoices):
    TOP = "top", "上装"
    BOTTOM = "bottom", "下装"
    OUTER = "outer", "外套"
    SHOES = "shoes", "鞋类"
    ACCESSORY = "accessory", "配饰"
    UNDERWEAR = "underwear", "内衣"


class Season(models.TextChoices):
    SPRING = "spring", "春季"
    SUMMER = "summer", "夏季"
    AUTUMN = "autumn", "秋季"
    WINTER = "winter", "冬季"
    ALL_SEASON = "all", "四季"


class Clothing(models.Model):
    """衣物"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clothes")
    name = models.CharField("名称", max_length=100)
    category = models.CharField("类别", max_length=20, choices=Category.choices)
    color = models.CharField("颜色", max_length=50, help_text="如：黑色、白色、藏蓝")
    brand = models.CharField("品牌", max_length=50, blank=True, default="")
    season = models.CharField(
        "适合季节", max_length=10, choices=Season.choices, default=Season.ALL_SEASON
    )
    image_url = models.URLField("图片URL", blank=True, default="")
    price = models.DecimalField(
        "价格", max_digits=10, decimal_places=2, null=True, blank=True
    )
    purchase_date = models.DateField("购买日期", null=True, blank=True)
    wear_count = models.IntegerField("穿着次数", default=0)
    is_favorite = models.BooleanField("是否收藏", default=False)
    notes = models.TextField("备注", blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "衣物"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class OutfitLog(models.Model):
    """穿搭日记 - 记录每天穿了什么"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="outfit_logs")
    date = models.DateField("日期")
    clothes = models.ManyToManyField(
        Clothing, verbose_name="穿搭衣物", related_name="outfit_logs"
    )
    occasion = models.CharField(
        "场合",
        max_length=50,
        blank=True,
        default="",
        help_text="如：上班、约会、运动、居家",
    )
    weather = models.CharField(
        "天气", max_length=50, blank=True, default="", help_text="如：晴 25C"
    )
    temperature = models.IntegerField("温度", null=True, blank=True)
    mood = models.CharField("心情", max_length=20, blank=True, default="")
    note = models.TextField("备注", blank=True, default="")
    photo_url = models.URLField("穿搭照URL", blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "穿搭日记"
        verbose_name_plural = verbose_name
        ordering = ["-date"]
        unique_together = ["user", "date"]

    def __str__(self):
        return f"{self.user.username} - {self.date} 穿搭"
