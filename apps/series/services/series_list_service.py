from django.db.models import QuerySet
from apps.series.models import Series
from apps.user.models import User


def get_my_series(*, user: User) -> QuerySet[Series]:
    """특정 유저(본인)가 만든 시리즈 목록을 조회하는 서비스 로직입니다."""

    # 1. Series 테이블에서 user 필드가 전달받은 user와 일치하는 데이터만 필터링(+ 최신순 정렬)
    return Series.objects.filter(user=user).order_by("-created_at")
