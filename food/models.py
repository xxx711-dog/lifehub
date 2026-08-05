"""食 - 饮食管理模块

核心功能：
- 菜谱库（分类、食材、步骤、营养标签）
- 每日餐食记录（早中晚餐 + 加餐）
- 智能推荐（根据偏好/食材/预算推荐菜谱）
- 购物清单（从菜谱自动生成）
"""

from django.contrib.auth.models import User
from django.db import models


class MealType(models.TextChoices):
    BREAKFAST = "breakfast", "早餐"
    LUNCH = "lunch", "午餐"
    DINNER = "dinner", "晚餐"
    SNACK = "snack", "加餐"


class Recipe(models.Model):
    """菜谱"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes", null=True, blank=True
    )
    title = models.CharField("菜名", max_length=100)
    category = models.CharField(
        "分类", max_length=30, help_text="如：家常菜、汤品、主食、凉菜、甜品"
    )
    cuisine = models.CharField(
        "菜系", max_length=20, blank=True, default="", help_text="如：川菜、粤菜、西餐"
    )
    difficulty = models.IntegerField("难度(1-5)", default=2)
    cook_time = models.IntegerField("烹饪时间(分钟)", default=30)
    servings = models.IntegerField("份数", default=2)
    calories = models.IntegerField("热量(大卡)", null=True, blank=True)
    budget = models.DecimalField(
        "预算(元)", max_digits=8, decimal_places=2, null=True, blank=True
    )

    ingredients = models.TextField("食材", help_text="每行一个：食材名 用量")
    steps = models.TextField("步骤", help_text="每行一个步骤")
    tags = models.CharField(
        "标签", max_length=200, blank=True, default="", help_text="逗号分隔"
    )

    is_public = models.BooleanField("公开菜谱", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "菜谱"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class MealLog(models.Model):
    """每日餐食记录"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meal_logs")
    date = models.DateField("日期")
    meal_type = models.CharField("餐次", max_length=20, choices=MealType.choices)
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, blank=True)
    custom_food = models.CharField(
        "自定义食物",
        max_length=200,
        blank=True,
        default="",
        help_text="非菜谱时的食物名",
    )
    calories = models.IntegerField("摄入热量(大卡)", null=True, blank=True)
    cost = models.DecimalField(
        "花费(元)", max_digits=8, decimal_places=2, null=True, blank=True
    )
    note = models.TextField("备注", blank=True, default="")
    rating = models.IntegerField("评分(1-5)", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "餐食记录"
        verbose_name_plural = verbose_name
        ordering = ["-date", "meal_type"]

    def __str__(self):
        food = self.recipe.title if self.recipe else self.custom_food
        return (
            f"{self.user.username} {self.date} {self.get_meal_type_display()}: {food}"
        )


class ShoppingItem(models.Model):
    """购物清单"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shopping_items"
    )
    name = models.CharField("物品名", max_length=100)
    quantity = models.CharField("数量", max_length=50, default="1")
    category = models.CharField(
        "分类",
        max_length=30,
        blank=True,
        default="",
        help_text="如：蔬菜、肉类、调味品、日用品",
    )
    is_purchased = models.BooleanField("已购买", default=False)
    estimated_price = models.DecimalField(
        "预估价格", max_digits=8, decimal_places=2, null=True, blank=True
    )
    actual_price = models.DecimalField(
        "实际价格", max_digits=8, decimal_places=2, null=True, blank=True
    )
    store = models.CharField("购买店铺", max_length=100, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    purchased_at = models.DateTimeField("购买时间", null=True, blank=True)

    class Meta:
        verbose_name = "购物清单"
        verbose_name_plural = verbose_name
        ordering = ["is_purchased", "-created_at"]

    def __str__(self):
        return f"{self.name} x{self.quantity}"
