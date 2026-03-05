from django.db.models import QuerySet
from apps.post.models import Post
from apps.user.models import User
from django.db.models import Count


def get_global_posts(
    series_id: int | None = None, tag_name: str | None = None
) -> QuerySet[Post]:
    """
    전체 피드 및 시리즈 목차, 태그 필터링용 포스트 목록을 가져옵니다.
    """
    # 1. 기본 필터링 조건 (임시글 제외, 공개글, 삭제되지 않은 글) 적용
    qs = Post.objects.filter(
        is_temp=False,
        visibility=Post.Visibility.PUBLIC,
        deleted_at__isnull=True,
    )

    # 2. 시리즈 ID가 전달되었다면 해당 시리즈의 글만 필터링
    if series_id:
        qs = qs.filter(series_id=series_id)

    # 3. 태그 이름이 전달되었다면, 연결된 태그의 이름이 일치하는 글만 필터링
    if tag_name:
        qs = qs.filter(tags__name=tag_name)

    # 4. N+1 문제 해결 및 좋아요 수 계산 후 생성일 기준 내림차순 정렬 반환
    return (
        qs.select_related("user")
        .prefetch_related("tags")
        .annotate(likes_count=Count("likes", distinct=True))
        .order_by("-created_at")
    )


def get_my_published_posts(
    *, user: User, series_id: int | None = None, tag_name: str | None = None
) -> QuerySet[Post]:
    """
    내가 작성한 발행 글 중 조건에 맞는 글만 가져옵니다.
    """
    # 1. 내 글 중 임시저장 및 삭제되지 않은 글 필터링
    qs = Post.objects.filter(
        user=user,
        is_temp=False,
        deleted_at__isnull=True,
    )

    # 2. 시리즈 ID 필터링
    if series_id:
        qs = qs.filter(series_id=series_id)

    # 3. 태그 이름 필터링 추가
    if tag_name:
        qs = qs.filter(tags__name=tag_name)

    # 4. N+1 문제 해결 및 좋아요 수 계산 후 반환
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
        .annotate(likes_count=Count("likes", distinct=True))
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
