from django.db.models import QuerySet, Q, Count, Subquery, OuterRef, IntegerField, Exists
from apps.post.models import Post, Like
from apps.user.models import User


def get_global_posts(
    series_id: int | None = None,
    tag_name: str | None = None,
    search_keyword: str | None = None,
) -> QuerySet[Post]:
    """
    전체 피드 및 시리즈 목차, 태그 필터링용 포스트 목록을 가져옵니다.
    """
    # 0. 서브쿼리 정의: "작성자의 총 게시글 수를 세어라" 라는 하위 작업 지시서를 만듬
    author_posts_count = (
        Post.objects.filter(
            # OuterRef("user_id"): 이 하위 작업 지시서가 '메인 쿼리'의 데이터와 연결되는 고리
            # "메인 쿼리에서 현재 보고 있는 그 게시글의 작성자(user_id)와 같은 사람의 글만 찾아라"
            user_id=OuterRef("user_id"),
            deleted_at__isnull=True
        )
        # user_id를 기준으로 데이터를 그룹화(GROUP BY)할 준비
        .values("user_id")
        # 그룹화된 데이터(각 유저)를 기준으로 게시글의 개수(id)를 세어 'count'라는 가상 필드를 만듬
        .annotate(count=Count("id"))
        # 메인 쿼리에 서브쿼리로 들어갈 때는 단일 값만 반환해야 하므로, 위에서 만든 'count' 필드만 결과로 추출
        .values("count")
    )

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

    # 4. 검색 기능 로직 추가
    if search_keyword:
        qs = qs.filter(
            Q(title__icontains=search_keyword)
            | Q(content__icontains=search_keyword)
            | Q(tags__name__icontains=search_keyword)
        ).distinct()  # 태그 M:N JOIN으로 인한 중복 결과 제거를 위해 추가

    # 5. N+1 문제 해결 및 좋아요 수 계산 후 생성일 기준 내림차순 정렬 반환
    return (
        # 메인 쿼리 실행
        qs.select_related("user", "series")
        .prefetch_related("tags")
        .annotate(
            # 중복되지 않은 좋아요(likes)의 개수를 세어 likes_count에 저장
            likes_count=Count("likes", distinct=True),
            # 3. 서브쿼리 결합: "게시글을 가져올 때, 위에서 만든 하위 작업 지시서(author_posts_count)도
            # 데이터베이스 안에서 같이 실행해서, 그 결과를 author_total_posts 라는 이름으로 붙여서 줘!"
            author_total_posts=Subquery(author_posts_count, output_field=IntegerField())
        )
        .order_by("-created_at")
    )


def get_my_published_posts(
    *,
    user: User,
    series_id: int | None = None,
    tag_name: str | None = None,
    search_keyword: str | None = None,
) -> QuerySet[Post]:
    """
    내가 작성한 발행 글 중 조건에 맞는 글만 가져옵니다.
    """
    # 0. 서브쿼리 정의: "작성자의 총 게시글 수를 세어라" 라는 하위 작업 지시서를 만듬
    author_posts_count = (
        Post.objects.filter(
            # OuterRef("user_id"): 이 하위 작업 지시서가 '메인 쿼리'의 데이터와 연결되는 고리
            # "메인 쿼리에서 현재 보고 있는 그 게시글의 작성자(user_id)와 같은 사람의 글만 찾아라"
            user_id=OuterRef("user_id"),
            deleted_at__isnull=True
        )
        # user_id를 기준으로 데이터를 그룹화(GROUP BY)할 준비
        .values("user_id")
        # 그룹화된 데이터(각 유저)를 기준으로 게시글의 개수(id)를 세어 'count'라는 가상 필드를 만듬
        .annotate(count=Count("id"))
        # 메인 쿼리에 서브쿼리로 들어갈 때는 단일 값만 반환해야 하므로, 위에서 만든 'count' 필드만 결과로 추출
        .values("count")
    )

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

    # 4. 검색 기능 로직 추가
    if search_keyword:
        # 제목(title), 내용(content), 태그이름(tags__name) 중 하나라도 검색어가 포함(icontains)되어 있는지 확인합니다.
        qs = qs.filter(
            Q(title__icontains=search_keyword)
            | Q(content__icontains=search_keyword)
            | Q(tags__name__icontains=search_keyword)
        ).distinct()

    # 5. N+1 문제 해결 및 좋아요 수 계산 후 반환
    return (
        # 메인 쿼리 실행
        qs.select_related("user", "series")
        .prefetch_related("tags")
        .annotate(
            # 중복되지 않은 좋아요(likes)의 개수를 세어 likes_count에 저장
            likes_count=Count("likes", distinct=True),
            # 3. 서브쿼리 결합: "게시글을 가져올 때, 위에서 만든 하위 작업 지시서(author_posts_count)도
            # 데이터베이스 안에서 같이 실행해서, 그 결과를 author_total_posts 라는 이름으로 붙여서 줘!"
            author_total_posts=Subquery(author_posts_count, output_field=IntegerField())
        )
        .order_by("-created_at")
    )


def get_my_temp_posts(*, user: User) -> QuerySet[Post]:
    """
    내가 작성한 임시 저장글 목록만 가져옵니다. (임시글 관리 페이지용)
    """
    # 1. 쿼리셋 생성: 로그인한 유저의 임시글 중 삭제되지 않은 글만 명확하게 필터링
    qs = Post.objects.filter(
        user=user,
        is_temp=True,
        deleted_at__isnull=True,
    )

    # 2. N+1 방지(JOIN 및 Prefetch) 적용 후 반환
    return (
        # 작성자(user)와 시리즈(series) 정보를 JOIN으로 한 번에 가져와 시리얼라이저 N+1 방지
        qs.select_related("user", "series")
        # 게시글에 달린 태그(tags) 정보도 IN 쿼리를 통해 한 번에 묶어서 가져옴
        .prefetch_related("tags")
        # 임시글은 최근에 작성/수정한 순서대로 보는 것이 편하므로 생성일 역순(최신순) 정렬 적용
        .order_by("-created_at")
    )


def get_post_detail(post_id: int, user: User | None = None) -> Post | None:
    """특정 ID의 게시글을 상세 조회합니다. (삭제되지 않은 글만)"""

    # 1. 서브쿼리: 작성자의 총 게시글 수 계산 (등급 이미지용)
    author_posts_count = (
        Post.objects.filter(
            user_id=OuterRef("user_id"),
            deleted_at__isnull=True
        )
        .values("user_id")
        .annotate(count=Count("id"))
        .values("count")
    )

    # 2. 메인 쿼리셋 생성 및 최적화 (N+1 방지 및 Annotation)
    qs = (
        Post.objects.filter(id=post_id, deleted_at__isnull=True)
        # [낭비 1 해결] 시리얼라이저의 N+1 쿼리 방지를 위해 "series" 조인 추가
        .select_related("user", "series")
        .prefetch_related("tags")
        .annotate(
            # 좋아요 개수 카운트
            likes_count=Count("likes", distinct=True),
            # [낭비 2 해결] 작성자의 총 게시글 수를 서브쿼리로 가져와 시리얼라이저 N+1 방지
            author_total_posts=Subquery(author_posts_count, output_field=IntegerField())
        )
    )

    # 3. [낭비 3 해결] 좋아요 여부(is_liked) 서브쿼리 처리
    if user and user.is_authenticated:
        # 현재 게시글(OuterRef("id"))에 현재 접속한 유저(user)가 좋아요를 눌렀는지 확인하는 서브쿼리
        is_liked_subquery = Like.objects.filter(
            post_id=OuterRef("id"),
            user=user
        )
        # Exists를 사용하면 조건에 맞는 데이터가 존재하면 True, 없으면 False를 'is_liked_by_user' 필드로 반환
        qs = qs.annotate(is_liked_by_user=Exists(is_liked_subquery))

    return qs.first()
