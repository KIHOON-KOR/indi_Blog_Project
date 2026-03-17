from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailSendSerializer(serializers.Serializer):
    # 입력값이 이메일 형식(text@test.com)인지 자동으로 검증해 주는 필드
    email = serializers.EmailField(
        required=True,
        # 형식이 틀렸을경우 보여줄 메세지
        error_messages={
            "invalid": "올바른 이메일 형식이 아닙니다.",
            "required": "이메일을 입력해주세요.",
        },
    )

    def validate_email(self, value):
        """입력된 이메일(value)에 대해 추가적인 정밀 검사를 수행"""
        # DB를 조회하여 해당 이메일로 이미 가입된 유저가 있는지 확인
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 가입된 이메일입니다.")
        return value


class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(
        required=True,
        max_length=6,
        min_length=6,
        error_messages={
            "required": "인증번호를 입력해주세요.",
            "max_length": "인증번호는 6자리입니다.",
            "min_length": "인증번호는 6자리입니다.",
        },
    )
