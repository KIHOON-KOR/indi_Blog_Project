from apps.comment.models import Comment
from apps.post.models import Post
from apps.user.models import User
from apps.core.exceptions.base import BaseCustomException
from apps.core.exceptions.messages import ErrorMessage


def create_comment(*, post_id: int, user: User, validated_data: dict) -> Comment:
    """댓글을 생성하는 서비스 로직입니다."""

    # 1. 대상 게시글이 존재하는지, 삭제되지 않았는지 검증
    post = Post.objects.filter(id=post_id, deleted_at__isnull=True).first()

    if not post:
        raise BaseCustomException(ErrorMessage.POST_NOT_FOUND)

    # 2. 댓글 생성 및 반환
    comment = Comment.objects.create(
        post=post, user=user, content=validated_data["content"]
    )

    return comment
