from typing import Any

from django.db import transaction
from apps.tags.models import Tag, PostTag
from apps.post.models import Post
from apps.user.models import User


@transaction.atomic
def create_post(*, author: User, validated_data: dict[str, Any]):
    """
    게시글을 생성하고 태그를 대량(Bulk)으로 처리하여 최적화한 로직입니다.
    """
    # 1. 입력 데이터에서 태그 목록을 분리합니다.
    tags_names = validated_data.pop("tags", [])

    # 2. 요약(summary)이 없을 경우 본문에서 앞부분을 추출하여 저장합니다.
    content = validated_data["content"]
    summary = validated_data.get("summary") or content[:150]

    # 3. 게시글을 먼저 생성합니다.
    post = Post.objects.create(
        user=author,
        title=validated_data["title"],
        content=content,
        summary=summary,
        thumbnail=validated_data.get("thumbnail"),
        is_temp=validated_data.get("is_temp", False),
    )

    # 4. 태그 최적화 처리 (N+1 문제 해결)
    if tags_names:
        # 4-1. 이미 존재하는 태그들을 한 번에 조회합니다.
        existing_tags = Tag.objects.filter(name__in=tags_names)
        existing_tag_names = {tag.name for tag in existing_tags}

        # 4-2. DB에 없는 새로운 태그들만 선별하여 한 번에 생성(bulk_create)합니다.
        new_tag_names = set(tags_names) - existing_tag_names
        if new_tag_names:
            Tag.objects.bulk_create([Tag(name=name) for name in new_tag_names])

        # 4-3. 연결할 모든 태그 객체를 다시 가져옵니다.
        all_tags = Tag.objects.filter(name__in=tags_names)

        # 4-4. PostTag(중간 테이블) 데이터도 bulk_create로 한 번에 저장합니다.
        PostTag.objects.bulk_create([PostTag(post=post, tag=tag) for tag in all_tags])

    return post
