from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

User = get_user_model()


class SignupService:
    """회원가입 관련 비즈니스 로직 클래스"""
    @staticmethod
    def create_user(validated_data: dict):
        """
        유효성 검사가 완료된 데이터를 받아 유저를 생성합니다.
        """
        email = validated_data.get("email")
        password = validated_data.get("password")
        nickname = validated_data.get("nickname")

        # 방어 로직 (문지기 역할)
        # 검증 서비스에서 만들어두었던 '인증 완료 딱지' 캐시 키
        verified_key = f"email_verified_{email}"
        # 레디스에 이 키가 존재하는지(True인지) 질문
        is_verified = cache.get(verified_key)

        if not is_verified:
            raise ValidationError("이메일 인증이 완료되지 않았습니다.")

        # 인증을 무사히 통과했다면 실제 유저를 DB에 생성
        user = User.objects.create_user(
            email=email,
            nickname=nickname,
            password=password,
            is_email_verified=True # 인증을 통과한 사람이므로 이메일 인증 여부를 True로 설정
        )

        # 보안 및 최적화(회원가입이 무사히 끝났으므로, 더 이상 필요 없는 인증 캐시를 레디스에서 삭제)
        cache.delete(verified_key)

        return user