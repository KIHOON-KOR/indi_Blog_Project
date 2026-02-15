from django.contrib.auth import get_user_model

User = get_user_model()


class SignupService:
    @staticmethod
    def create_user(validated_data: dict):
        """
        유효성 검사가 완료된 데이터를 받아 유저를 생성합니다.
        """
        email = validated_data.get("email")
        password = validated_data.get("password")
        nickname = validated_data.get("nickname")

        user = User.objects.create_user(
            email=email, nickname=nickname, password=password
        )

        return user
