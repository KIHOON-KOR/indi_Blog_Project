from apps.user.models import User
from django.db import transaction
from apps.core.exceptions.messages import ErrorMessage
from apps.comment.models import Comment
from apps.core.exceptions.base import BaseCustomException


@transaction.atomic
def delete_comment(*, comment_id: int, user: User) -> None:
    """댓글을 삭제하는 서비스 로직입니다."""

    # 1. 대상 댓글 조회
    comment = Comment.objects.filter(id=comment_id).first()

    # 2. 권한 검증(댓글 존재여부)
    if not comment:
        raise BaseCustomException(ErrorMessage.COMMENT_NOT_FOUND)

    # 3. 권한 검증(댓글 작성자 여부)
    if comment.user != user:
        raise BaseCustomException(ErrorMessage.NOT_COMMENT_AUTHOR)

    # 4. 데이터베이스에서 댓글 삭제
    comment.delete()
