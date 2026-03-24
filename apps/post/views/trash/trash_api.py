from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema
from typing import cast

from apps.post.services.trash.post_trash_service import (
    get_trashed_posts,
    get_trashed_post_detail,
    restore_trashed_post,
    hard_delete_post,
)
from apps.post.views.mixins import PostListMixin
from apps.user.models import User
from apps.post.serializers.post_list import PostListSerializer
from apps.post.serializers.post_detail import PostDetailSerializer
from apps.core.pagination import PostPageNumberPagination


class TrashAPIView(APIView, PostListMixin):
    """휴지통 목록 조회를 담당합니다."""

    permission_classes = [IsAuthenticated]
    pagination_class = PostPageNumberPagination

    @extend_schema(tags=["휴지통"], summary="휴지통 목록 조회")
    def get(self, request: Request):
        # 1. 요청한 유저 객체를 가져옴
        user = cast(User, request.user)
        # 2. 서비스 레이어를 호출
        posts = get_trashed_posts(user=user)

        # 3. 페이지네이션을 적용하여 응답
        return self.get_paginated_response(
            queryset=posts,
            serializer_class=PostListSerializer,
            request=request,
            context={"request": request}
        )


class TrashManageAPIView(APIView):
    """휴지통 내 게시글 상세 확인, 복구, 영구 삭제를 담당합니다."""

    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["휴지통"], summary="휴지통 게시글 상세 조회")
    def get(self, request: Request, post_id: int):
        # 1. 서비스레이어 호출
        post = get_trashed_post_detail(post_id=post_id, user=cast(User, request.user))
        return Response(PostDetailSerializer(post, context={"request": request}).data)

    @extend_schema(tags=["휴지통"], summary="휴지통 게시글 복구")
    def patch(self, request: Request, post_id: int):
        # 1. 서비스 레이어를 호출
        restore_trashed_post(post_id=post_id, user=cast(User, request.user))
        return Response(
            {"message": "게시글이 성공적으로 복구되었습니다."},
            status=status.HTTP_200_OK,
        )

    @extend_schema(tags=["휴지통"], summary="휴지통 게시글 영구 삭제")
    def delete(self, request: Request, post_id: int):
        # 1. 서비스 레이어를 호출
        hard_delete_post(post_id=post_id, user=cast(User, request.user))
        return Response(status=status.HTTP_204_NO_CONTENT)
