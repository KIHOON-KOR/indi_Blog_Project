from django.db.models import QuerySet
from apps.post.models import Post
from apps.user.models import User
from apps.core.exceptions.base import BaseCustomException
from apps.core.exceptions.messages import ErrorMessage


def get_trashed_posts(*, user: User) -> QuerySet[Post]:
    """사용자의 삭제된 게시글(휴지통) 목록을 조회합니다."""
    # 본인이 작성한 글 중, deleted_at 필드가 비어있지 않은(삭제된) 데이터만 가져옴(내림차순 정렬)
    return Post.objects.filter(
        user=user,
        deleted_at__isnull=False
    ).order_by("-deleted_at")


def get_trashed_post_detail(*, post_id: int, user: User) -> Post:
    """휴지통 내 특정 게시글의 상세 내용을 조회합니다."""
    # 삭제된 상태의 글인지 명확히 확인하기 위해 deleted_at__isnull=False 조건을 줌
    post = Post.objects.filter(
        id=post_id,
        user=user,
        deleted_at__isnull=False
    ).first()

    if not post:
        raise BaseCustomException(ErrorMessage.POST_NOT_FOUND)

    return post


def restore_trashed_post(*, post_id: int, user: User) -> Post:
    """휴지통에 있는 게시글을 원래 상태로 복구합니다."""
    # 복구할 대상을 찾음
    post = get_trashed_post_detail(post_id=post_id, user=user)

    # deleted_at 필드를 None으로 초기화하여 Soft Delete 상태를 해제
    post.deleted_at = None
    post.save(update_fields=["deleted_at"])

    return post


def hard_delete_post(*, post_id: int, user: User) -> None:
    """휴지통에 있는 게시글을 DB에서 영구 삭제합니다."""
    # 영구 삭제할 대상을 찾음
    post = get_trashed_post_detail(post_id=post_id, user=user)

    # DB에서 완전히 물리적 삭제를 진행
    post.delete()