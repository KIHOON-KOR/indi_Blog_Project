from drf_spectacular.utils import extend_schema, OpenApiParameter
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
from drf_spectacular.types import OpenApiTypes
from .mixins import PostListMixin



class PostAPIView(APIView, PostListMixin):
    """포스트 등록 및 전체 목록 조회를 담당합니다."""

    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostPageNumberPagination

    @extend_schema(
        tags=["포스트"],
        summary="전체 포스트 피드 조회",
        parameters=[
            OpenApiParameter(
                name="series",
                description="필터링할 시리즈 ID",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
            ),
            OpenApiParameter(
                name="tag",
                description="필터링할 태그 이름",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
            ),
            OpenApiParameter(
                name="search",
                description="제목, 내용, 태그 기준 검색 키워드",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
            ),
        ],
    )
    def get(self, request: Request):
        # 1. Mixin의 메서드를 호출하여 복잡했던 쿼리 파라미터 파싱 로직을 단 한 줄로 처리
        filter_params = self.get_filter_params(request)

        # 2. 서비스 레이어 함수를 호출할 때, 딕셔너리 언패킹(**)을 사용하여 인자를 매우 깔끔하게 전달
        posts = get_global_posts(**filter_params)

        # 3. Mixin의 페이지네이션 메서드를 호출하여 결과물(Response)을 바로 반환
        return self.get_paginated_response(
            queryset=posts,                      # 페이징할 대상 데이터
            serializer_class=PostListSerializer, # 직렬화에 사용할 시리얼라이저 클래스
            request=request                      # 현재 요청 객체
        )

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


class MyPostAPIView(APIView, PostListMixin):
    """내 블로그(공개글만) 조회를 담당합니다."""

    permission_classes = [IsAuthenticated]
    pagination_class = PostPageNumberPagination

    @extend_schema(
        tags=["포스트"],
        summary="내 블로그 공개글 조회",
        parameters=[
            OpenApiParameter(
                name="series",
                description="필터링할 시리즈 ID",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
            ),
            OpenApiParameter(
                name="tag",
                description="필터링할 태그 이름",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
            ),
            OpenApiParameter(
                name="search",
                description="제목, 내용, 태그 기준 검색 키워드",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
            ),
        ],
    )
    def get(self, request: Request):
        # 1. User 타입 지정
        user = cast(User, request.user)

        # 2. Mixin을 통해 중복되던 쿼리 파라미터 파싱 로직을 한 줄로 대체합니다.
        filter_params = self.get_filter_params(request)

        # 3. 서비스 레이어 호출 시 작성자(user) 인자와 파싱된 파라미터(**filter_params)를 함께 전달합니다.
        posts = get_my_published_posts(user=user, **filter_params)

        # 4. 페이지네이션 처리 및 응답 반환 역시 Mixin을 활용하여 한 줄로 압축합니다.
        return self.get_paginated_response(
            queryset=posts,
            serializer_class=PostListSerializer,
            request=request
        )


class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(tags=["포스트"], summary="게시글 상세 조회")
    def get(self, request: Request, post_id: int):
        # 1. 서비스 레이어를 호출할 때 request.user도 함께 넘겨줌
        post = get_post_detail(post_id, user=request.user)  # type: ignore

        # 2. 게시글이 없는 경우 예외 발생
        if not post:
            raise BaseCustomException(ErrorMessage.POST_NOT_FOUND)

        # 3. 데이터 반환
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
