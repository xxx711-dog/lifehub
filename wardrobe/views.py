"""wardrobe views"""

from django.db.models import Q
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Clothing, OutfitLog
from .serializers import ClothingSerializer, OutfitLogSerializer


class ClothingListCreateView(generics.ListCreateAPIView):
    serializer_class = ClothingSerializer

    def get_queryset(self):
        qs = Clothing.objects.filter(user=self.request.user)
        category = self.request.query_params.get("category")
        season = self.request.query_params.get("season")
        if category:
            qs = qs.filter(category=category)
        if season:
            qs = qs.filter(Q(season=season) | Q(season="all"))
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ClothingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClothingSerializer

    def get_queryset(self):
        return Clothing.objects.filter(user=self.request.user)


class OutfitLogListCreateView(generics.ListCreateAPIView):
    serializer_class = OutfitLogSerializer

    def get_queryset(self):
        qs = OutfitLog.objects.filter(user=self.request.user)
        date = self.request.query_params.get("date")
        if date:
            qs = qs.filter(date=date)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OutfitLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OutfitLogSerializer

    def get_queryset(self):
        return OutfitLog.objects.filter(user=self.request.user)


class WardrobeSuggestView(APIView):
    """根据天气/场合智能推荐穿搭"""

    def get(self, request):
        user = request.user
        temperature = request.query_params.get("temperature")
        occasion = request.query_params.get("occasion", "")

        season = None
        clothes = Clothing.objects.filter(user=user)
        if temperature:
            try:
                t = int(temperature)
                if t <= 10:
                    season = "winter"
                elif t <= 20:
                    season = "autumn"
                elif t <= 25:
                    season = "spring"
                else:
                    season = "summer"
                clothes = clothes.filter(Q(season=season) | Q(season="all"))
            except ValueError:
                pass

        # 从各类别中推荐收藏的优先
        result = {}
        for cat in ["top", "bottom", "outer", "shoes"]:
            items = clothes.filter(category=cat).order_by(
                "-is_favorite", "-wear_count"
            )[:3]
            result[cat] = ClothingSerializer(items, many=True).data

        return Response(
            {
                "temperature": temperature,
                "season_filter": season,
                "occasion": occasion,
                "suggestions": result,
            }
        )
