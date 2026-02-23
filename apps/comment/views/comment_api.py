from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema
from typing import cast

from apps.comment.serializers.create_comment_serializer import CommentCreateSerializer
from apps.comment.services.create_comment_service import create_comment
from apps.user.models import User


class CommentAPIView(APIView):
    """게시글의 댓글 작성을 담당하는 View입니다."""

    # 로그인한 유저만 댓글을 작성할 수 있도록 설정
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["댓글"], summary="댓글 작성", request=CommentCreateSerializer)
    def post(self, request: Request, post_id: int):
        # 1. 입력 데이터 검증
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. User 타입 캐스팅 (기존 코드 컨벤션 적용)
        user = cast(User, request.user)

        # 3. 서비스 레이어 호출
        create_comment(
            post_id=post_id, user=user, validated_data=serializer.validated_data
        )

        # 4. 성공 응답 반환
        return Response(
            {"message": "댓글이 성공적으로 작성되었습니다."},
            status=status.HTTP_201_CREATED,
        )
