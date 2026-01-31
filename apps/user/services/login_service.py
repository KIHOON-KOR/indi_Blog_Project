from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions

class UserService:
    @staticmethod
    def authenticate_user(email, password):
        # 1. Django의 authenticate를 통해 자격 증명을 확인합니다.
        # User 모델에 정의된 USERNAME_FIELD('email')를 기준으로 인증합니다.
        user = authenticate(email=email, password=password)

        # 2. 인증 실패 시 예외를 발생시켜 서비스 흐름을 중단합니다.
        if not user:
            raise exceptions.AuthenticationFailed("이메일 또는 비밀번호가 일치하지 않습니다.")
        
        # 3. 비활성화된 계정인지 확인합니다.
        if not user.is_active:
            raise exceptions.PermissionDenied("해당 계정은 비활성화 상태입니다.")

        # 4. 성공 시 JWT 토큰을 생성합니다.
        refresh = RefreshToken.for_user(user)
        
        # 5. 필요한 데이터 구조를 반환합니다.
        return {
            "user": user,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }