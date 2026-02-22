from rest_framework import serializers
from apps.post.models import Post


class PostDetailSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source="user.nickname", read_only=True)

    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")  # type: ignore
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "thumbnail",
            "author_nickname",
            "created_at",
            "visibility",
            "tags",
            "likes_count",
        ]
