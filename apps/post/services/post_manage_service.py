from django.utils import timezone
from apps.tags.models import Tag, PostTag
from apps.core.exceptions.base import BaseCustomException
from apps.post.models import Post
from apps.user.models import User
from apps.core.exceptions.messages import ErrorMessage
from django.db import transaction

def restore_temp_post(post_id: int, user: User):
    """임시글을 공개글로 전환(복구)합니다."""
    post = Post.objects.filter(id=post_id, user=user, is_temp=True).first()

    if not post:
        raise BaseCustomException(ErrorMessage.POST_NOT_FOUND)

    post.is_temp = False
    post.save(update_fields=["is_temp"])


def soft_delete_post(post_id: int, user: User):
    """게시글을 삭제(Soft Delete) 처리합니다."""
    post = Post.objects.filter(id=post_id, user=user, deleted_at__isnull=True).first()

    if not post:
        raise BaseCustomException(ErrorMessage.POST_NOT_FOUND)

    post.deleted_at = timezone.now()
    post.save(update_fields=["deleted_at"])


@transaction.atomic
def update_post(*, post_id: int, user: User, validated_data: dict):
    # 1. 권한 확인 및 존재 여부 확인
    post = Post.objects.filter(id=post_id, user=user, deleted_at__isnull=True).first()

    # 게시글이 존재하지 않거나 권한이 없는 경우
    if not post:
        raise BaseCustomException(ErrorMessage.POST_NOT_FOUND)

    # 2. 태그 데이터가 있다면 데이터에서 태그 목록을 추출
    tag_names = validated_data.pop("tags", None)

    # 3. 전달된 데이터로 게시글 필드를 업데이트
    for attr, value in validated_data.items():
        setattr(post, attr, value)

    # 요약이 비어있다면 본문에서 자동으로 추출
    if not validated_data.get("summary"):
        post.summary = post.content[:150]

    post.save()

    # 4. 태그가 전달되었다면 기존 관계를 끊고 새로 생성(최적화)
    if tag_names is not None:
        post.posttag_set.all().delete()  # 기존의 PostTag 중간 테이블 관계를 모두 삭제

        # 신규 태그 생성 및 연결
        existing_tags = Tag.objects.filter(name__in=tag_names)  # 이미 DB에 있는 태그를 조회
        existing_names = {t.name for t in existing_tags}  # 조회된 태그 이름들을 셋(Set)으로 만듬

        new_names = set(tag_names) - existing_names  # DB에 없는 새로운 태그 이름들만 골라냅니다.
        if new_names:  # 새로 추가할 태그가 있다면 한 번에 생성
            Tag.objects.bulk_create([Tag(name=name) for name in new_names])

        all_tags = Tag.objects.filter(name__in=tag_names)  # 전체 태그 객체들을 다시 가져옴
        PostTag.objects.bulk_create([PostTag(post=post, tag=tag) for tag in all_tags])  # 게시글과 연결

    return post

def delete_post(post_id: int, user: User):
    # 1. 본인의 게시글 중 삭제되지 않은 글을 찾음
    post = Post.objects.filter(id=post_id, user=user, deleted_at__isnull=True).first()

    # 대상이 없거나 권한이 없는 경우
    if not post:
        raise BaseCustomException(ErrorMessage.POST_NOT_FOUND)

    # 2. 삭제 일시를 현재 시간으로 설정하여 논리적 삭제 처리
    post.deleted_at = timezone.now() # deleted_at 필드에 현재 시각을 기록
    post.save(update_fields=["deleted_at"])