from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.request import Request
from typing import cast
from apps.comment.serializers.create_comment_serializer import CommentCreateSerializer
from apps.comment.services.update_comment_service import update_comment
from apps.user.models import User
from rest_framework.response import Response
from rest_framework import status


class CommentManageAPIView(APIView):
    """게시글의 댓글 수정/삭제을 담당하는 View입니다."""

    # 로그인한 유저만 댓글을 작성할 수 있도록 설정
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        tags=["댓글"],
        summary="게시글 댓글 수정",
        request=CommentCreateSerializer,
    )
    def put(self, request: Request, comment_id: int):
        # 1. 입력 데이터 검증
        serializer = CommentCreateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # 2. User 타입 지정
        user = cast(User, request.user)

        # 3. 서비스 레이어 호출
        comment = update_comment(
            comment_id=comment_id, user=user, validated_data=serializer.validated_data
        )

        # 4. 성공 응답 반환
        return Response(
            CommentCreateSerializer(comment).data,
            status=status.HTTP_200_OK,
        )
