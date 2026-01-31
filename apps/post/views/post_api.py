from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.request import Request
from typing import cast

from apps.post.services.post_create_service import create_post
from apps.user.models import User
from apps.post.serializers.post_create import PostCreateSerializer


class PostAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["포스트"],
        summary="포스트 등록 API",
        request=PostCreateSerializer,
    )
    def post(self, request: Request):
        # 1. 입력 데이터 검증
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. 유저 타입 캐스팅 (Type Hinting)
        user = cast(User, request.user)

        # 3. 서비스레이어 호출
        post = create_post(
            author=user,
            validated_data=serializer.validated_data,
        )

        # 4. 응답 반환
        return Response(
            {"id": post.id, "message": "질문이 성공적으로 등록되었습니다."},
            status=status.HTTP_201_CREATED,
        )