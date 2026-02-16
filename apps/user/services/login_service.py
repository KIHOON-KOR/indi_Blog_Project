from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from apps.core.exceptions.base import BaseCustomException
from apps.core.exceptions.messages import ErrorMessage


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
            raise BaseCustomException(ErrorMessage.LOGIN_FAILED)

        # 3. 계정 활성화 여부를 확인
        if not user.is_active:
            raise BaseCustomException(ErrorMessage.USER_INACTIVE)

        # 4. JWT 토큰 생성
        refresh = RefreshToken.for_user(user)

        # 5. 최종 결과 반환
        return {
            "user": user,
            "access_token": str(refresh.access_token),  # Access Token 문자열
            "refresh_token": str(refresh),  # Refresh Token 문자열
        }
