from rest_framework import serializers


# 로그인 시 입력받을 데이터와 검증 로직을 담당하는 시리얼라이저입니다.
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
