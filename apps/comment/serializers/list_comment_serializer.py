from rest_framework import serializers
from apps.comment.models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    """댓글 목록 조회를 위한 시리얼라이저입니다."""

    author_nickname = serializers.CharField(source="user.nickname", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "author_nickname",
            "content",
            "created_at",
        ]
