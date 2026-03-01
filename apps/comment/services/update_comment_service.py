from typing import Any
from apps.user.models import User
from django.db import transaction
from apps.core.exceptions.messages import ErrorMessage
from apps.comment.models import Comment
from apps.core.exceptions.base import BaseCustomException


@transaction.atomic
def update_comment(
    *, comment_id: int, user: User, validated_data: dict[str, Any]
) -> Comment:
    """댓글을 수정하는 서비스 로직입니다."""

    # 1. 대상 댓글이 존재하는지 검증
    comment = Comment.objects.filter(id=comment_id).first()

    # 2. 권한 검증(댓글 존재여부)
    if not comment:
        raise BaseCustomException(ErrorMessage.COMMENT_NOT_FOUND)

    # 3. 권한 검증(댓글 작성자 여부)
    if comment.user != user:
        raise BaseCustomException(ErrorMessage.NOT_COMMENT_AUTHOR)

    # 4. 데이터 업데이트
    if "content" in validated_data:
        comment.content = validated_data["content"]
        comment.save(update_fields=["content"])

    return comment  # type: ignore
