from django.db import IntegrityError
from apps.series.models import Series
from apps.user.models import User
from apps.core.exceptions.base import BaseCustomException
from apps.core.exceptions.messages import ErrorMessage


def create_series(*, user: User, name: str) -> Series:
    """새로운 시리즈를 생성하는 서비스 로직입니다."""

    try:
        # 1. 전달받은 user와 name으로 새로운 Series 객체를 데이터베이스에 생성
        series = Series.objects.create(user=user, name=name)

        # 2. 생성된 객체 반환
        return series

    # 3. UniqueConstraint(user, name) 제약 조건(시리즈 이름 중복)
    except IntegrityError:
        raise BaseCustomException(ErrorMessage.SERIES_ALREADY_EXISTS)
