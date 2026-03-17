from rest_framework import serializers

class PasswordResetRequestSerializer(serializers.Serializer):
    """비밀번호 재설정 '요청(메일 발송)'을 검증하는 시리얼라이저"""
    email = serializers.EmailField(
        required=True,
        error_messages={"invalid": "올바른 이메일 형식이 아닙니다.", "required": "이메일을 입력해주세요."}
    )

class PasswordResetConfirmSerializer(serializers.Serializer):
    """비밀번호 '변경(인증번호 확인)'을 검증하는 시리얼라이저"""
    email = serializers.EmailField(required=True)
    code = serializers.CharField(
        required=True,
        max_length=6,
        min_length=6,
        error_messages={"required": "인증번호를 입력해주세요.", "max_length": "인증번호는 6자리입니다.", "min_length": "인증번호는 6자리입니다."}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True, # 보안을 위해 쓰기 전용으로 설정 (응답으로 내려가지 않음)
        error_messages={"required": "새 비밀번호를 입력해주세요."}
    )