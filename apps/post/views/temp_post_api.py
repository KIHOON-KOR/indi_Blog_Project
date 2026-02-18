from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from typing import cast

from apps.post.services.post_list_service import (
    get_my_temp_posts,
)
from apps.post.services.post_manage_service import restore_temp_post, soft_delete_post
from apps.user.models import User
from apps.post.serializers.post_list import PostListSerializer
from apps.core.pagination import PostPageNumberPagination


class MyTempAPIView(APIView):
    """임시 저장글 조회를 담당합니다."""

    permission_classes = [IsAuthenticated]
    pagination_class = PostPageNumberPagination

    @extend_schema(tags=["임시저장"], summary="임시 저장글 목록 조회")
    def get(self, request: Request):
        user = cast(User, request.user)
        # 임시글 관리 페이지를 위해 is_temp=True인 글만 가져옵니다.
        posts = get_my_temp_posts(user=user)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(posts, request, view=self)

        if page is not None:
            return paginator.get_paginated_response(
                PostListSerializer(page, many=True).data
            )

        return Response(PostListSerializer(posts, many=True).data)


class MyTempManageAPIView(APIView):
    """임시 저장글 관리(복구/삭제)를 담당합니다."""

    permission_classes = [IsAuthenticated]
    pagination_class = PostPageNumberPagination

    @extend_schema(tags=["임시저장"], summary="임시 저장글 복구")
    def patch(self, request: Request, post_id: int):
        # 임시글 상태를 해제하여 공개글로 전환합니다.
        restore_temp_post(post_id=post_id, user=cast(User, request.user))
        return Response(
            {"message": "포스트가 발행되었습니다."}, status=status.HTTP_200_OK
        )

    @extend_schema(tags=["임시저장"], summary="임시 저장글 삭제")
    def delete(self, request: Request, post_id: int):
        soft_delete_post(post_id=post_id, user=cast(User, request.user))
        return Response(status=status.HTTP_204_NO_CONTENT)
