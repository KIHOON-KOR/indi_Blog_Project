from apps.post.models import Post
from apps.post.models.like import Like
from apps.user.models import User
from apps.core.exceptions.base import BaseCustomException
from apps.core.exceptions.messages import ErrorMessage
from django.db import IntegrityError


def add_post_like(*, post_id: int, user: User) -> None:
    """게시글 좋아요를 등록하는 서비스 로직입니다."""

    # 1. 대상 게시글이 존재하는지, 삭제되지 않았는지 확인
    post = Post.objects.filter(id=post_id, deleted_at__isnull=True).first()

    if not post:
        raise BaseCustomException(ErrorMessage.POST_NOT_FOUND)

    # 2. Like 객체를 가져오거나 생성
    try:
        Like.objects.get_or_create(post=post, user=user)
    except IntegrityError:
        # 이미 좋아요가 눌려있는 경우의 안전한 처리
        pass


def remove_post_like(*, post_id: int, user: User) -> None:
    """게시글 좋아요를 삭제(취소)하는 서비스 로직입니다."""

    # 1. 삭제 시에도 대상 게시글이 유효한지 검증
    post = Post.objects.filter(id=post_id, deleted_at__isnull=True).first()

    if not post:
        raise BaseCustomException(ErrorMessage.POST_NOT_FOUND)

    # 2. 좋아요 객체를 삭제
    Like.objects.filter(post=post, user=user).delete()
