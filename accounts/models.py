"""用户账户模型 - 用户扩展 + 个人偏好"""

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """用户扩展信息"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar_color = models.CharField("头像颜色", max_length=7, default="#6C5CE7")
    nickname = models.CharField("昵称", max_length=50, blank=True, default="")
    city = models.CharField("所在城市", max_length=50, blank=True, default="")
    bio = models.TextField("个人简介", blank=True, default="")

    # 衣 - 身体数据
    height = models.IntegerField("身高(cm)", null=True, blank=True)
    weight = models.IntegerField("体重(kg)", null=True, blank=True)

    # 食 - 饮食偏好
    diet_preference = models.CharField(
        "饮食偏好",
        max_length=20,
        blank=True,
        default="",
        help_text="如：素食、低碳水、高蛋白、无限制",
    )
    allergy = models.TextField("过敏食物", blank=True, default="")

    # 住 - 预算
    monthly_budget = models.DecimalField(
        "月度预算", max_digits=10, decimal_places=2, null=True, blank=True
    )

    # 行 - 通勤
    commute_mode = models.CharField(
        "通勤方式",
        max_length=20,
        blank=True,
        default="",
        help_text="如：地铁、公交、自驾、骑行、步行",
    )
    commute_minutes = models.IntegerField("通勤时长(分钟)", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "用户档案"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username} 的档案"
