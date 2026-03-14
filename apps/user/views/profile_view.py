from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from typing import cast

from apps.user.models import User
from apps.user.services.users_stat_service import get_user_garden_stats
from apps.user.serializers.profile_serializer import UserProfileResponseSerializer


class UserProfileAPIView(APIView):
    """마이페이지 상단에 표시될 유저 프로필 및 활동 통계 정보를 제공합니다."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["회원관리"],
        summary="마이페이지 프로필 조회",
        responses={200: UserProfileResponseSerializer}
    )
    def get(self, request):
        # 1. User 타입 지정
        user = cast(User, request.user)

        # 2. 서비스 레이어를 호출
        stats_data = get_user_garden_stats(user)

        # 3. 시리얼라이저에 넣을 원본 데이터를 딕셔너리 형태로 조립
        raw_data = {
            "user_info": {
                "email": user.email,
                "nickname": user.nickname,
                "profile_img": user.profile_img,
                "bio": user.bio,
            },
            "stats": {
                "total_post_count": stats_data["total_count"],
                "current_grade": stats_data["current_grade"],
                "next_grade": stats_data["next_grade"],
                "progress_percent": stats_data["progress_percent"],
            }
        }

        # 4. 조립된 데이터를 시리얼라이저에 넣어 검증 및 직렬화(JSON 변환 준비)를 수행
        serializer = UserProfileResponseSerializer(instance=raw_data)

        # 5. 시리얼라이징된 안전한 데이터를 클라이언트(프론트엔드)에 반환
        return Response(serializer.data)