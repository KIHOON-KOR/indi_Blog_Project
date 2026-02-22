from rest_framework import serializers
from apps.post.models import Post


class PostListSerializer(serializers.ModelSerializer):
    """목록 조회를 위한 시리얼라이저"""

    author_nickname = serializers.CharField(source="user.nickname", read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "thumbnail",
            "author_nickname",
            "created_at",
            "visibility",
            "likes_count",
        ]
