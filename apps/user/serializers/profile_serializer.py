from rest_framework import serializers
from apps.user.models import User


# 1. 유저 기본 정보를 담을 중첩 시리얼라이저
class UserInfoSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="유저 이메일")
    nickname = serializers.CharField(help_text="유저 닉네임")
    profile_img = serializers.CharField(
        allow_null=True, required=False, help_text="프로필 이미지 URL"
    )
    bio = serializers.CharField(allow_null=True, required=False, help_text="자기소개")


# 2. 유저 통계 정보를 담을 중첩 시리얼라이저
class UserStatsSerializer(serializers.Serializer):
    total_post_count = serializers.IntegerField(help_text="총 작성 글 개수")
    current_grade = serializers.DictField(help_text="현재 등급 정보")
    next_grade = serializers.DictField(
        allow_null=True, help_text="다음 등급 정보 (최고 레벨이면 null)"
    )
    progress_percent = serializers.IntegerField(help_text="다음 등급까지의 진행률(%)")


# 3. 최종적으로 마이페이지에 응답할 최상단 시리얼라이저
class UserProfileResponseSerializer(serializers.Serializer):
    user_info = UserInfoSerializer(help_text="유저 기본 정보")
    stats = UserStatsSerializer(help_text="유저 활동 통계")


# 4. 프로필 수정을 위해 요청 데이터를 검증할 시리얼라이저
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 클라이언트가 수정할 수 있도록 허용할 필드들만 리스트로 명시
        fields = ["nickname", "profile_img", "bio"]
        # 모든 필드를 필수가 아니게(partial update) 만들어 일부만 수정할 수 있게 함
        extra_kwargs = {
            "nickname": {"required": False},  # 닉네임 생략 가능
            "profile_img": {"required": False},  # 프로필 이미지 생략 가능
            "bio": {"required": False},  # 자기소개 생략 가능
        }


# 5. 타인에게 보여질 공개용 기본 정보 시리얼라이저 (이메일 제외)
class PublicUserInfoSerializer(serializers.Serializer):
    nickname = serializers.CharField(help_text="유저 닉네임")
    # 프로필 이미지는 없을 수도 있으므로 allow_null 처리
    profile_img = serializers.CharField(
        allow_null=True, required=False, help_text="프로필 이미지 URL"
    )
    # 자기소개 역시 없을 수 있으므로 allow_null 처리
    bio = serializers.CharField(allow_null=True, required=False, help_text="자기소개")


# 6. 공개용 프로필 최종 응답 시리얼라이저
class PublicUserProfileResponseSerializer(serializers.Serializer):
    user_info = PublicUserInfoSerializer(help_text="유저 공개 정보")
    stats = UserStatsSerializer(help_text="유저 활동 통계")
