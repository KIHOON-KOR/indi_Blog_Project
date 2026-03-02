from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema
from typing import cast

from apps.user.models import User
from apps.series.serializers import SeriesCreateSerializer, SeriesListSerializer
from apps.series.services.series_list_service import get_my_series
from apps.series.services.series_manage_service import create_series


class SeriesAPIView(APIView):
    """내 시리즈 목록 조회 및 생성을 담당하는 View입니다."""

    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["시리즈"], summary="내 시리즈 목록 조회")
    def get(self, request: Request):
        # 1. User 타입 지정
        user = cast(User, request.user)

        # 2. 서비스 레이어 호출
        series_list = get_my_series(user=user)

        # 3. 데이터 직렬화 및 응답
        serializer = SeriesListSerializer(series_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["시리즈"], summary="새 시리즈 생성", request=SeriesCreateSerializer
    )
    def post(self, request: Request):
        # 1. 입력 데이터 검증
        serializer = SeriesCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. User 타입 지정
        user = cast(User, request.user)

        # 3. 서비스 레이어 호출 (시리즈 생성)
        series = create_series(user=user, name=serializer.validated_data["name"])

        # 4. 생성 완료 응답
        return Response(
            {"id": series.id, "message": "시리즈가 성공적으로 생성되었습니다."},
            status=status.HTTP_201_CREATED,
        )
