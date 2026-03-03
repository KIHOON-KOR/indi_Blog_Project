from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from typing import cast
from apps.series.serializers import SeriesCreateSerializer
from apps.series.services.series_manage_service import update_series, delete_series
from rest_framework.request import Request
from apps.user.models import User

class SeriesDetailAPIView(APIView):
    """특정 시리즈의 수정 및 삭제를 담당하는 View입니다."""

    # 로그인한 사용자만 접근 가능하도록 권한 설정
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["시리즈"], summary="시리즈 수정", request=SeriesCreateSerializer
    )
    def put(self, request: Request, series_id: int):
        # 1. 입력데이터 검증
        serializer = SeriesCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. User 타입 지정
        user = cast(User, request.user)

        # 3. 서비스 레이어 호출
        updated_series = update_series(
            series_id=series_id,
            user=user,
            name=serializer.validated_data["name"]
        )

        return Response(
            {"id": updated_series.id, "message": "시리즈가 성공적으로 수정되었습니다."},
            status=status.HTTP_200_OK,
        )

    @extend_schema(tags=["시리즈"], summary="시리즈 삭제")
    def delete(self, request: Request, series_id: int):
        # 1. User 타입 지정
        user = cast(User, request.user)

        # 2. 서비스 레이어 호출
        delete_series(series_id=series_id, user=user)

        return Response(status=status.HTTP_204_NO_CONTENT)