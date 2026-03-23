from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from apps.user.serializers.login_serializer import LoginSerializer
from apps.user.services.login_service import UserService


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    # 해당 뷰에 IP 기반으로 요청 횟수를 제한하는 ScopedRateThrottle을 장착
    throttle_classes = [ScopedRateThrottle]

    # settings.py에 정의된 'login_attempt' (예: 5/min) 룰을 적용하도록 이름을 매칭
    throttle_scope = 'login_attempt'

    @extend_schema(
        tags=["회원관리"],
        summary="이메일 로그인",
        request=LoginSerializer,
    )
    def post(self, request):
        # 1. 입력 데이터 검증
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. 서비스 레이어 호출
        login_data = UserService.authenticate_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        # 3. 최종 성공 응답을 반환합니다.
        return Response(
            {
                "message": "로그인에 성공하였습니다.",
                "token": {
                    "access": login_data["access_token"],
                    "refresh": login_data["refresh_token"],
                },
                "user": {
                    "email": login_data["user"].email,
                    "nickname": login_data["user"].nickname,
                },
            },
            status=status.HTTP_200_OK,
        )
