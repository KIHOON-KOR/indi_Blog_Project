from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema
from typing import cast

from apps.comment.serializers.create_comment_serializer import CommentCreateSerializer
from apps.comment.serializers.list_comment_serializer import CommentListSerializer
from apps.comment.services.create_comment_service import create_comment
from apps.comment.services.list_comment_service import get_post_comments
from apps.core.pagination import PostPageNumberPagination
from apps.user.models import User


class CommentAPIView(APIView):
    """게시글의 댓글 작성을 담당하는 View입니다."""

    # 로그인한 유저만 댓글을 작성할 수 있도록 설정
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostPageNumberPagination

    @extend_schema(tags=["댓글"], summary="게시글 댓글 목록 조회")
    def get(self, request: Request, post_id: int):
        """GET 요청 시 특정 게시글의 댓글 목록을 페이지네이션하여 반환합니다."""

        # 1. 서비스 레이어를 호출
        comments = get_post_comments(post_id=post_id)

        # 2. 페이지네이션 객체를 생성
        paginator = self.pagination_class()

        # 3. 받아온 쿼리셋을 현재 request의 쿼리 파라미터(예: ?page=1)에 맞게 자름
        page = paginator.paginate_queryset(comments, request, view=self)

        if page is not None:
            serializer = CommentListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response(CommentListSerializer(comments, many=True).data)

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
