from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from typing import cast

from apps.user.models import User
from apps.user.services.profile_service import (
    get_public_profile,
    check_nickname_available,
)
from apps.user.services.users_stat_service import get_user_garden_stats
from apps.user.serializers.profile_serializer import (
    UserProfileResponseSerializer,
    UserProfileUpdateSerializer,
    PublicUserProfileResponseSerializer,
)


class UserProfileAPIView(APIView):
    """마이페이지 상단에 표시될 유저 프로필 및 활동 통계 정보를 제공합니다."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["회원관리"],
        summary="마이페이지 프로필 조회",
        responses={200: UserProfileResponseSerializer},
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
            },
        }

        # 4. 조립된 데이터를 시리얼라이저에 넣어 검증 및 직렬화(JSON 변환 준비)를 수행
        serializer = UserProfileResponseSerializer(instance=raw_data)

        # 5. 시리얼라이징된 안전한 데이터를 클라이언트(프론트엔드)에 반환
        return Response(serializer.data)

    @extend_schema(
        tags=["회원관리"],
        summary="마이페이지 프로필 수정",
        request=UserProfileUpdateSerializer,  # Swagger 문서에 어떤 형태의 요청이 필요한지 명시합니다.
        responses={
            200: UserProfileResponseSerializer
        },  # 수정 성공 시 최신 프로필 데이터를 반환함을 명시합니다.
    )
    def patch(self, request):
        # 1. User 타입 지정
        user = cast(User, request.user)

        # 2. 시리얼라이저 호출
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # 3. DB 업데이트
        serializer.save()

        # 4. 프로필 업데이트가 완료되었으니, 수정된 최신 상태의 프로필을 다시 응답해 주기 위해 GET 로직과 동일하게 통계를 조회
        stats_data = get_user_garden_stats(user)

        # 5. 응답할 데이터를 조립
        raw_data = {
            "user_info": {
                "email": user.email,
                "nickname": user.nickname,
                "profile_img": user.profile_img,  # 방금 업데이트된 S3 프로필 이미지 주소가 들어감
                "bio": user.bio,
            },
            "stats": {
                "total_post_count": stats_data["total_count"],
                "current_grade": stats_data["current_grade"],
                "next_grade": stats_data["next_grade"],
                "progress_percent": stats_data["progress_percent"],
            },
        }

        # 6. 응답용 시리얼라이저에 조립한 데이터를 넣어 검증
        response_serializer = UserProfileResponseSerializer(instance=raw_data)

        return Response(response_serializer.data)


class PublicUserProfileAPIView(APIView):
    """특정 닉네임을 가진 사용자의 공개 프로필 및 활동 통계 정보를 제공합니다."""

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["회원관리"],
        summary="타인 공개 프로필 조회 (닉네임 기반)",
        responses={200: PublicUserProfileResponseSerializer},
    )
    def get(self, request, nickname):
        # 1. 서비스레이어 호출
        raw_data = get_public_profile(nickname)

        # 2. 서비스 레이어에서 가져온 딕셔너리 데이터를 시리얼라이저에 넣어 JSON 형태로 직렬화 준비
        serializer = PublicUserProfileResponseSerializer(instance=raw_data)

        return Response(serializer.data)


class CheckNicknameAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. URL에 포함된 '?nickname=값' 에서 값을 꺼냄
        nickname = request.query_params.get("nickname", "").strip()

        # 2. 만약 닉네임이 비어있다면, 뷰 단에서 즉시 에러를 반환합니다.
        if not nickname:
            return Response({"detail": "닉네임을 입력해주세요."}, status=400)

        # 3. 서비스레이어 호출
        is_available, detail_message = check_nickname_available(request.user, nickname)

        return Response({"is_available": is_available, "detail": detail_message})
