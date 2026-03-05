from django.db.models import QuerySet, Count, Q
from apps.tags.models import Tag
from apps.post.models import Post

def get_tags_with_post_counts(user=None) -> QuerySet[Tag]:
    """태그 목록과 각 태그별 유효한 게시글 수를 반환하는 서비스 로직입니다."""

    # 1. 태그 개수를 집계하기 위한 기본 필터 조건을 Q 객체로 정의합니다.
    filter_conditions = Q(
        posts__is_temp=False, # 임시 저장된 글은 제외
        posts__deleted_at__isnull=True, # 휴지통에 들어간(삭제된) 글 제외
    )

    # 2. 만약 인자로 user 객체가 넘어왔고, 그 유저가 인증된 사용자라면
    if user and user.is_authenticated:
        # 조건에 '해당 유저가 작성한 글'이라는 조건을 AND(&=)로 추가 결합
        filter_conditions &= Q(posts__user=user.id)
    else:
        # 전체 공개(PUBLIC) 상태인 게시글만 통계에 포함되도록 조건을 추가
        filter_conditions &= Q(posts__visibility=Post.Visibility.PUBLIC)

    # 3. 위에서 만든 필터 조건을 바탕으로 카운트(개수 세기) 기준을 생성
    valid_post_count = Count(
        "posts",  # 태그 모델과 연결된 Post 모델을 참조
        filter=filter_conditions, # 위에서 만든 필터 조건을 적용하여 개수를 카운트
        distinct=True,  # 동일한 게시글이 여러 번 세어지는 것을 방지(중복 제거)
    )

    # 4. 최종적으로 조건이 반영된 태그 목록을 데이터베이스에서 가져와 반환
    return (
        Tag.objects.annotate( # 태그 객체에 새로운 가상의 필드를 추가
            post_count=valid_post_count # 위에서 만든 카운트 기준을 'post_count'라는 이름의 필드로 저장
        )
        .filter(post_count__gt=0)  # 게시글 수가 0개 초과(즉, 1개 이상)인 태그들만 남김
        .order_by( # 정렬 기준을 지정
            "-post_count", "name" # 첫 번째 기준: 개수 내림차순(많은 순), 두 번째 기준: 태그 이름 오름차순(가나다순)
        )
    )