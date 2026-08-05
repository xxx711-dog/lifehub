"""wardrobe serializers"""

from django.db import models
from rest_framework import serializers
from .models import Clothing, OutfitLog


class ClothingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothing
        fields = "__all__"
        read_only_fields = ["user", "wear_count", "created_at", "updated_at"]


class OutfitLogSerializer(serializers.ModelSerializer):
    clothes = ClothingSerializer(many=True, read_only=True)
    clothes_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = OutfitLog
        fields = "__all__"
        read_only_fields = ["user", "created_at"]

    def create(self, validated_data):
        clothes_ids = validated_data.pop("clothes_ids", [])
        outfit = OutfitLog.objects.create(**validated_data)
        if clothes_ids:
            outfit.clothes.set(clothes_ids)
            # 更新穿着次数
            Clothing.objects.filter(id__in=clothes_ids).update(
                wear_count=models.F("wear_count") + 1
            )
        return outfit

    def update(self, instance, validated_data):
        clothes_ids = validated_data.pop("clothes_ids", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if clothes_ids is not None:
            instance.clothes.set(clothes_ids)
        return instance
