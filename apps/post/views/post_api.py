from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from typing import cast
from apps.core.exceptions.messages import ErrorMessage
from apps.core.exceptions.base import BaseCustomException
from apps.post.serializers.post_detail import PostDetailSerializer
from apps.post.services.post_create_service import create_post
from apps.post.services.post_list_service import (
    get_global_posts,
    get_my_published_posts,
    get_post_detail,
)
from apps.post.services.post_manage_service import update_post, delete_post
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
        # 1. URL에서 '?series=숫자' 값을 꺼내옵니다.
        series_id_str = request.query_params.get("series")
        series_id = int(series_id_str) if series_id_str and series_id_str.isdigit() else None

        # 2. 서비스 레이어 호출 시 series_id를 전달합니다.
        posts = get_global_posts(series_id=series_id)

        # 3. 페이지네이션 적용
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
        # 1. 입력 데이터 검증
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. User 타입 지정
        user = cast(User, request.user)

        # 3. 서비스 레이어 호출
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
        # 1. User 타입 지정
        user = cast(User, request.user)

        # 2. URL에서 '?series=숫자' 파라미터 값을 꺼내옴
        series_id_str = request.query_params.get("series")
        series_id = int(series_id_str) if series_id_str and series_id_str.isdigit() else None

        # 3. 서비스 레이어 호출
        posts = get_my_published_posts(user=user, series_id=series_id)

        # 4. 페이지 네이션 적용
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(posts, request, view=self)

        if page is not None:
            return paginator.get_paginated_response(
                PostListSerializer(page, many=True).data
            )

        return Response(PostListSerializer(posts, many=True).data)


class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(tags=["포스트"], summary="게시글 상세 조회")
    def get(self, request: Request, post_id: int):
        # 1. 서비스 레이어를 호출
        post = get_post_detail(post_id)

        # 2. 게시글이 없는 경우(None), 커스텀 예외를 발생
        if not post:
            raise BaseCustomException(ErrorMessage.POST_NOT_FOUND)

        # 이렇게 해야 Serializer 내부에서 현재 접속한 유저가 누구인지 알 수 있음
        return Response(PostDetailSerializer(post, context={"request": request}).data)

    @extend_schema(tags=["포스트"], summary="게시글 수정", request=PostCreateSerializer)
    def put(self, request: Request, post_id: int):
        # 1. 입력 데이터 검증
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. User 타입 지정
        user = cast(User, request.user)

        # 3. 서비스 레이어 호출
        updated_post = update_post(
            post_id=post_id, user=user, validated_data=serializer.validated_data
        )

        return Response(
            PostCreateSerializer(updated_post).data, status=status.HTTP_200_OK
        )

    @extend_schema(tags=["포스트"], summary="게시글 삭제(Soft Delete)")
    def delete(self, request: Request, post_id: int):
        # 1. User 타입 지정
        user = cast(User, request.user)

        # 2. 서비스 레이어 호출
        delete_post(post_id=post_id, user=user)

        return Response(status=status.HTTP_204_NO_CONTENT)
