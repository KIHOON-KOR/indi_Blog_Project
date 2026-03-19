from typing import Any

from django.db import transaction
from apps.core.exceptions.messages import ErrorMessage
from apps.core.exceptions.base import BaseCustomException
from apps.tags.models import Tag, PostTag
from apps.post.models import Post
from apps.user.models import User


@transaction.atomic
def create_post(*, author: User, validated_data: dict[str, Any]):
    """
    게시글을 생성하고 태그를 대량(Bulk)으로 처리하여 최적화한 로직입니다.
    """
    # 1. 입력 데이터에서 태그 목록을 분리
    tags_names = validated_data.pop("tags", [])

    # 2. 클라이언트가 전달한 시리즈 객체를 뽑음 (없으면 None)
    series = validated_data.pop("series", None)

    # 전달받은 시리즈가 있다면, 그 시리즈를 만든 사람(user)이 현재 글 작성자(author)와 일치하는지 확인
    if series and series.user != author:
        raise BaseCustomException(ErrorMessage.SERIES_PERMISSION_DENIED)

    # 3. 요약(summary)이 없을 경우 본문에서 앞부분을 추출하여 저장
    content = validated_data["content"]
    summary = validated_data.get("summary") or content[:150]

    # 4. 게시글을 먼저 생성
    post = Post.objects.create(
        user=author,
        title=validated_data["title"],
        content=content,
        summary=summary,
        thumbnail=validated_data.get("thumbnail"),
        is_temp=validated_data.get("is_temp", False),
        visibility=validated_data.get("visibility", Post.Visibility.PUBLIC),
        series=series,
    )

    # 5. 태그 최적화 처리 (N+1 문제 해결)
    if tags_names:
        # 5-1. 이미 존재하는 태그들을 한 번에 조회
        existing_tags = Tag.objects.filter(name__in=tags_names)
        existing_tag_names = {tag.name for tag in existing_tags}

        # 5-2. DB에 없는 새로운 태그들만 선별하여 한 번에 생성(bulk_create)
        new_tag_names = set(tags_names) - existing_tag_names
        if new_tag_names:
            Tag.objects.bulk_create([Tag(name=name) for name in new_tag_names])

        # 4-3. 연결할 모든 태그 객체를 다시 가져옴
        all_tags = Tag.objects.filter(name__in=tags_names)

        # 4-4. PostTag(중간 테이블) 데이터도 bulk_create로 한 번에 저장
        PostTag.objects.bulk_create([PostTag(post=post, tag=tag) for tag in all_tags])

    return post
