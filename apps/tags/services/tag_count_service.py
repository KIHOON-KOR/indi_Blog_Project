from django.db.models import QuerySet, Count, Q
from apps.tags.models import Tag
from apps.post.models import Post


def get_tags_with_post_counts() -> QuerySet[Tag]:
    """태그 목록과 각 태그별 유효한 게시글 수를 반환하는 서비스 로직입니다."""

    # 1. 집계(Count)할 조건을 명확히 설정합니다.
    valid_post_count = Count(
        "posts",  # Tag 관점에서 연관된 Post의 related_name
        filter=Q(
            posts__is_temp=False,
            posts__deleted_at__isnull=True,
            posts__visibility=Post.Visibility.PUBLIC,
        ),
        distinct=True,  # 중복 카운팅을 방지합니다.
    )

    # 2. Tag 쿼리셋을 만듭니다.
    return (
        Tag.objects.annotate(
            post_count=valid_post_count
        )  # 각 태그마다 'post_count'라는 가상 컬럼을 붙여 개수를 계산합니다.
        .filter(post_count__gt=0)  # 게시글이 0개인 껍데기 태그는 필터링합니다.
        .order_by(
            "-post_count", "name"
        )  # 게시글이 많은 태그부터 내림차순 정렬하고, 개수가 같으면 이름순으로 정렬합니다.
    )
