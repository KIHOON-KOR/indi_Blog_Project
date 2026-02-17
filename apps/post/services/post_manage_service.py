from django.utils import timezone
from django.shortcuts import get_object_or_404
from apps.post.models import Post
from apps.user.models import User

def restore_temp_post(post_id: int, user: User):
    """임시글을 공개글로 전환(복구)합니다."""
    post = get_object_or_404(Post, id=post_id, user=user, is_temp=True)
    post.is_temp = False
    post.save()

def soft_delete_post(post_id: int, user: User):
    """게시글을 삭제(Soft Delete) 처리합니다."""
    post = get_object_or_404(Post, id=post_id, user=user, deleted_at__isnull=True)
    post.deleted_at = timezone.now()
    post.save()