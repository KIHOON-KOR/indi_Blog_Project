from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from typing import cast

from apps.post.services.post_create_service import create_post
from apps.post.services.post_list_service import (
    get_global_posts,
    get_my_published_posts,
)
from apps.user.models import User
from apps.post.serializers.post_create import PostCreateSerializer
from apps.post.serializers.post_list import PostListSerializer
from apps.core.pagination import PostPageNumberPagination


class PostAPIView(APIView):
    """포스트 등록 및 전체 목록 조회를 담당합니다."""

    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostPageNumberPagination

    @extend_schema(tags=["포스트"], summary="전체 포스트 피드 조회")
    def get(self, request: Request):
        # 1. 서비스 레이어에서 전체 공개글 쿼리셋을 가져옵니다.
        posts = get_global_posts()
        # 2. 커스텀 페이지네이션을 적용합니다.
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(posts, request, view=self)

        if page is not None:
            serializer = PostListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response(PostListSerializer(posts, many=True).data)

    @extend_schema(
        tags=["포스트"], summary="포스트 등록 API", request=PostCreateSerializer
    )
    def post(self, request: Request):
        """기존 작성하신 등록 로직 유지"""
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = cast(User, request.user)
        post = create_post(author=user, validated_data=serializer.validated_data)
        return Response(
            {"id": post.id, "message": "성공적으로 등록되었습니다."},
            status=status.HTTP_201_CREATED,
        )


class MyPostAPIView(APIView):
    """내 블로그(공개글만) 조회를 담당합니다."""

    permission_classes = [IsAuthenticated]
    pagination_class = PostPageNumberPagination

    @extend_schema(tags=["포스트"], summary="내 블로그 공개글 조회")
    def get(self, request: Request):
        user = cast(User, request.user)
        # 내 블로그에서는 내가 쓴 '공개된' 글만 필터링합니다.
        posts = get_my_published_posts(user=user)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(posts, request, view=self)

        if page is not None:
            return paginator.get_paginated_response(
                PostListSerializer(page, many=True).data
            )

        return Response(PostListSerializer(posts, many=True).data)
