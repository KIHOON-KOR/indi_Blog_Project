from rest_framework import serializers

from apps.post.models import Post
from apps.series.models import Series


class PostCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,  # 태그는 없을 수도 있음
        write_only=True,  # 저장할 때만 사용 (응답에는 포함 X)
    )
    series = serializers.PrimaryKeyRelatedField(
        queryset=Series.objects.all(),  # 존재하는 모든 시리즈 중에서 찾도록 쿼리셋 지정
        required=False,  # 시리즈 지정은 필수가 아니므로 False
        allow_null=True,  # 빈 값도 허용하여 시리즈 없이도 글을 쓸 수 있게 함
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "thumbnail",
            "summary",
            "is_temp",
            "tags",
            "visibility",
            "series",
        ]
        # 특정 필드에 대한 추가 설정을 지정
        extra_kwargs = {
            "summary": {
                "required": False,
                "allow_blank": True,
            },  # 요약은 필수가 아니며 빈 값도 허용
            "is_temp": {"default": False},  # 기본적으로는 정식 발행(False) 상태로 처리
        }
