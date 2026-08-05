"""图片上传接口"""

import uuid
import os
from pathlib import Path

from django.conf import settings
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


class ImageUploadView(APIView):
    """通用图片上传接口

    POST /api/upload/
    字段: image (文件), folder (可选, 默认 'general')
    返回: {url: '/media/folder/xxx.jpg'}
    """

    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        image = request.FILES.get("image")
        if not image:
            return Response(
                {"error": "请提供图片文件"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 限制类型和大小
        allowed = ["image/jpeg", "image/png", "image/webp", "image/gif"]
        if image.content_type not in allowed:
            return Response(
                {"error": f"仅支持 {', '.join(allowed)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if image.size > 5 * 1024 * 1024:
            return Response(
                {"error": "图片大小超过 5MB"}, status=status.HTTP_400_BAD_REQUEST
            )

        folder = request.data.get("folder", "general")
        # 只允许安全路径
        safe_folders = {"wardrobe", "travel", "general", "avatar"}
        if folder not in safe_folders:
            folder = "general"

        # 生成唯一文件名
        ext = Path(image.name).suffix.lower()
        if ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
            ext = ".jpg"
        filename = f"{uuid.uuid4().hex}{ext}"

        # 保存路径
        upload_dir = Path(settings.MEDIA_ROOT) / folder
        upload_dir.mkdir(parents=True, exist_ok=True)
        filepath = upload_dir / filename

        with open(filepath, "wb+") as dest:
            for chunk in image.chunks():
                dest.write(chunk)

        url = f"{settings.MEDIA_URL}{folder}/{filename}"
        return Response({"url": url}, status=status.HTTP_201_CREATED)
