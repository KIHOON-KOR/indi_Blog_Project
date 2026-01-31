from typing import Any

from django.db import transaction
from apps.tags.models import Tag, PostTag
from apps.post.models import Post
from apps.user.models import User

@transaction.atomic
def create_post(*, author: User, validated_data: dict[str, Any]):
    """
    게시글을 생성하는 비즈니스 로직입니다.
    """
    tags_names = validated_data.pop("tags", [])

    post = Post.objects.create(
        user=author,
        title=validated_data["title"],
        content=validated_data["content"],
        thumbnail=validated_data.get("thumbnail"),
    )

    if tags_names:
        for name in tags_names:
            tag, created = Tag.objects.get_or_create(name=name)

            PostTag.objects.create(post=post, tag=tag)
    return post
