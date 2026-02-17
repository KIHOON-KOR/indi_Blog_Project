from django.db.models import QuerySet  # QuerySet 타입을 힌팅하기 위해 임포트합니다.
from apps.post.models import Post  # Post 모델을 사용하기 위해 임포트합니다.
from apps.user.models import User  # User 모델을 사용하기 위해 임포트합니다.


def get_global_posts() -> QuerySet[Post]:
    """
    모든 사용자의 공개된 포스트 목록을 가져옵니다. (전체 피드용)
    """
    return (
        Post.objects.filter(
            is_temp=False,  # 임시 저장글은 제외합니다.
            deleted_at__isnull=True,  # 삭제되지 않은 글만 필터링합니다.
        )
        .select_related("user")
        .order_by("-created_at")
    )  # 작성자 정보를 JOIN하고 최신순으로 정렬합니다.


def get_my_published_posts(*, user: User) -> QuerySet[Post]:
    """
    내가 작성한 글 중 공개된(발행된) 글만 가져옵니다. (내 블로그용)
    """
    return (
        Post.objects.filter(
            user=user,  # 현재 로그인한 유저의 글만 필터링합니다.
            is_temp=False,  # 발행된 글만 가져옵니다.
            deleted_at__isnull=True,  # 삭제되지 않은 글만 필터링합니다.
        )
        .select_related("user")
        .order_by("-created_at")
    )  # 성능을 위해 유저 정보를 미리 가져옵니다.


def get_my_temp_posts(*, user: User) -> QuerySet[Post]:
    """
    내가 작성한 임시 저장글 목록만 가져옵니다. (임시글 관리 페이지용)
    """
    return Post.objects.filter(
        user=user,  # 내 글 중에서
        is_temp=True,  # 임시 저장 상태인 글만 필터링합니다.
        deleted_at__isnull=True,  # 아직 삭제되지 않은 글이어야 합니다.
    ).order_by(
        "-created_at"
    )  # 최신순으로 정렬합니다.
