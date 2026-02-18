from django.utils import timezone

from apps.core.exceptions.base import BaseCustomException
from apps.post.models import Post
from apps.user.models import User
from apps.core.exceptions.messages import ErrorMessage


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
