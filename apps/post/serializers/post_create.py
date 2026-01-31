from rest_framework import serializers

from apps.post.models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,  # 태그는 없을 수도 있음
        write_only=True  # 저장할 때만 사용 (응답에는 포함 X)
    )
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "thumbnail",
            "tags",
        ]