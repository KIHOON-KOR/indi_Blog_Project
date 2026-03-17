from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.user.serializers.password_serializer import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from apps.user.services.password_service import PasswordResetService


class PasswordResetRequestView(APIView):
    """비밀번호 재설정 '인증번호 발송'을 처리하는 뷰"""

    permission_classes = [AllowAny]

    def post(self, request):
        # 1. 입력데이터 검증
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. 검사를 무사히 통과한 깨끗한 이메일을 가져옴
        email = serializer.validated_data.get("email")

        # 3. 서비스레이어 호출
        PasswordResetService.send_reset_code(email)

        return Response(
            {"message": "비밀번호 재설정 인증번호가 발송되었습니다."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    """비밀번호 '변경 (인증번호 확인)'을 처리하는 뷰"""

    permission_classes = [AllowAny]

    def post(self, request):
        # 1. 입력데이터 검증
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")  # 검증된 이메일을 꺼냄
        code = serializer.validated_data.get("code")  # 검증된 6자리 인증번호를 꺼냄
        new_password = serializer.validated_data.get(
            "new_password"
        )  # 검증된 새로운 비밀번호를 꺼냄

        # 2. 서비스레이어 호출
        PasswordResetService.reset_password(email, code, new_password)

        return Response(
            {"message": "비밀번호가 성공적으로 변경되었습니다."},
            status=status.HTTP_200_OK,
        )
