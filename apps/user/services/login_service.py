from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions


class UserService:
    @staticmethod
    def authenticate_user(email, password):
        """
        사용자 인증 및 JWT 토큰 생성을 담당하는 메서드입니다.
        """

        # 1. Django 기본 인증 함수(authenticate)를 사용
        user = authenticate(email=email, password=password)

        # 2. 인증 실패 시(user가 None일 경우) 예외를 발생시킵니다.
        if not user:
            raise exceptions.AuthenticationFailed(
                "이메일 또는 비밀번호가 일치하지 않습니다."
            )

        # 3. 계정 활성화 여부를 확인
        if not user.is_active:
            raise exceptions.PermissionDenied("해당 계정은 비활성화 상태입니다.")

        # 4. JWT 토큰 생성
        refresh = RefreshToken.for_user(user)

        # 5. 최종 결과 반환
        return {
            "user": user,
            "access_token": str(refresh.access_token),  # Access Token 문자열
            "refresh_token": str(refresh),  # Refresh Token 문자열
        }