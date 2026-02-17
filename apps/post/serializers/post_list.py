from rest_framework import serializers
from apps.post.models import Post


class PostListSerializer(serializers.ModelSerializer):
    """목록 조회를 위한 시리얼라이저"""

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "thumbnail",
            "created_at",
        ]