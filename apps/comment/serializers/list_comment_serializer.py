from rest_framework import serializers
from apps.comment.models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    """댓글 목록 조회를 위한 시리얼라이저입니다."""

    author_nickname = serializers.CharField(source="user.nickname", read_only=True)
    author_profile_image = serializers.CharField(
        source="user.profile_img", read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "author_nickname",
            "author_profile_image",
            "content",
            "created_at",
        ]
