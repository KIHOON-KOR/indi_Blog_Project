from rest_framework import serializers

# 1. 유저 기본 정보를 담을 중첩 시리얼라이저
class UserInfoSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="유저 이메일")
    nickname = serializers.CharField(help_text="유저 닉네임")
    profile_img = serializers.CharField(allow_null=True, required=False, help_text="프로필 이미지 URL")
    bio = serializers.CharField(allow_null=True, required=False, help_text="자기소개")

# 2. 유저 통계 정보를 담을 중첩 시리얼라이저
class UserStatsSerializer(serializers.Serializer):
    total_post_count = serializers.IntegerField(help_text="총 작성 글 개수")
    current_grade = serializers.DictField(help_text="현재 등급 정보")
    next_grade = serializers.DictField(allow_null=True, help_text="다음 등급 정보 (최고 레벨이면 null)")
    progress_percent = serializers.IntegerField(help_text="다음 등급까지의 진행률(%)")

# 3. 최종적으로 마이페이지에 응답할 최상단 시리얼라이저
class UserProfileResponseSerializer(serializers.Serializer):
    user_info = UserInfoSerializer(help_text="유저 기본 정보")
    stats = UserStatsSerializer(help_text="유저 활동 통계")