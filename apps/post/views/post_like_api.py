from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema
from typing import cast

from apps.user.models import User
from apps.post.services.post_like_service import add_post_like, remove_post_like


class PostLikeAPIView(APIView):
    """게시글 좋아요 등록 및 삭제를 담당하는 View입니다."""
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["포스트 좋아요"], summary="게시글 좋아요 등록")
    def post(self, request: Request, post_id: int):
        """POST 요청이 오면 좋아요를 생성합니다."""
        # 1. User 타입 지정
        user = cast(User, request.user)

        # 2. 서비스 레이어 호출
        add_post_like(post_id=post_id, user=user)

        return Response(
            {"message": "좋아요가 등록되었습니다."},
            status=status.HTTP_201_CREATED
        )

    @extend_schema(tags=["포스트 좋아요"], summary="게시글 좋아요 취소(삭제)")
    def delete(self, request: Request, post_id: int):
        """DELETE 요청이 오면 좋아요를 삭제합니다."""

        # 1. User 타입 지정
        user = cast(User, request.user)

        # 2. 서비스 레이어 호출
        remove_post_like(post_id=post_id, user=user)

        return Response(status=status.HTTP_204_NO_CONTENT)