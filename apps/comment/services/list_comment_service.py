from django.db.models import QuerySet
from apps.comment.models import Comment
from apps.post.models import Post
from apps.core.exceptions.base import BaseCustomException
from apps.core.exceptions.messages import ErrorMessage


def get_post_comments(*, post_id: int) -> QuerySet[Comment]:
    """특정 게시글의 댓글 목록을 조회하는 서비스 로직입니다."""

    # 1. 대상 게시글이 유효한지 검증(존재여부 확인)
    post_exists = Post.objects.filter(id=post_id, deleted_at__isnull=True).exists()

    if not post_exists:
        raise BaseCustomException(ErrorMessage.POST_NOT_FOUND)

    # 2. 댓글 목록 조회 및 반환
    comments = (
        Comment.objects.filter(post_id=post_id)
        .select_related("user")
        .order_by("created_at")
    )

    return comments