from django.db.models import QuerySet
from apps.post.models import Post
from apps.user.models import User
from django.db.models import Count


def get_global_posts(series_id: int | None = None) -> QuerySet[Post]:
    """
    모든 사용자의 공개된 포스트 목록을 가져옵니다. (전체 피드 및 시리즈 목차용)
    """
    qs = Post.objects.filter(
        is_temp=False,
        visibility=Post.Visibility.PUBLIC,
        deleted_at__isnull=True,
    )

    # 시리즈 ID가 전달되었다면 해당 시리즈의 글만 필터링합니다.
    if series_id:
        qs = qs.filter(series_id=series_id)

    return (
        qs.select_related("user")
        .prefetch_related("tags")
        .annotate(likes_count=Count("likes", distinct=True))
        .order_by("-created_at")
    )


def get_my_published_posts(
    *, user: User, series_id: int | None = None
) -> QuerySet[Post]:
    """
    내가 작성한 글 중 공개된(발행된) 글만 가져옵니다. (내 블로그용)
    """
    qs = Post.objects.filter(
        user=user,
        is_temp=False,
        deleted_at__isnull=True,
    )

    # 전달받은 시리즈 아이디가 있다면 필터링 적용
    if series_id:
        qs = qs.filter(series_id=series_id)

    return (
        qs.select_related("user")
        .prefetch_related("tags")
        .annotate(likes_count=Count("likes", distinct=True))
        .order_by("-created_at")
    )


def get_my_temp_posts(*, user: User) -> QuerySet[Post]:
    """
    내가 작성한 임시 저장글 목록만 가져옵니다. (임시글 관리 페이지용)
    """
    return (
        Post.objects.filter(
            user=user,
            is_temp=True,
            deleted_at__isnull=True,
        )
        .prefetch_related("tags")
        .order_by("-created_at")
    )


def get_post_detail(post_id: int) -> Post:
    """
    특정 ID의 게시글을 상세 조회합니다. (삭제되지 않은 글만)
    """
    return (
        Post.objects.select_related("user")  # type: ignore
        .filter(id=post_id, deleted_at__isnull=True)
        .prefetch_related("tags")
        .annotate(likes_count=Count("likes", distinct=True))
        .first()
    )
