from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8  # 최소 8자 이상
    )

    class Meta:
        model = User
        # 클라이언트로부터 입력받을 필드
        fields = ['email', 'nickname', 'password']

    def validate_email(self, value):
        """
        이메일 중복 여부를 검증합니다.
        Model의 unique=True가 있지만, 여기서 명시적인 에러 메시지를 주는 것이 UX에 좋습니다.
        """
        # 해당 이메일로 가입된 유저가 있는지 DB에서 확인
        if User.objects.filter(email=value).exists():
            # 이미 존재한다면 유효성 검사 에러(400)를 발생
            raise serializers.ValidationError("이미 존재하는 이메일입니다.")
        # 문제가 없다면 입력받은 이메일 값을 그대로 반환
        return value