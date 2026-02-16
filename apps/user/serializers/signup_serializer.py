from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.core.exceptions.base import BaseCustomException
from apps.core.exceptions.messages import ErrorMessage

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        min_length=8,  # 최소 8자 이상
    )

    class Meta:
        model = User
        # 클라이언트로부터 입력받을 필드
        fields = ["email", "nickname", "password"]

    def validate_email(self, value):
        """
        이메일 중복 여부를 검증합니다.
        """
        # 해당 이메일로 가입된 유저가 있는지 DB에서 확인
        if User.objects.filter(email=value).exists():
            raise BaseCustomException(ErrorMessage.EMAIL_ALREADY_EXISTS)
        return value
