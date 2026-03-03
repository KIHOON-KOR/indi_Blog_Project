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


def update_series(*, series_id: int, user: User, name: str) -> Series:
    """기존 시리즈의 이름을 변경하는 서비스 로직입니다."""

    # 1. 전달받은 series_id와 user 정보로 내 시리즈가 맞는지 데이터베이스에서 조회합니다.
    series = Series.objects.filter(id=series_id, user=user).first()

    # 2. 조회된 시리즈가 없다면 (남의 것이거나 없는 ID일 경우) 에러를 발생시킵니다.
    if not series:
        raise BaseCustomException(ErrorMessage.SERIES_SERVICE_PERMISSION)

    try:
        # 3. 모델 객체의 이름을 새로운 이름으로 변경
        series.name = name

        # 4. 변경된 이름만 데이터베이스에 업데이트
        series.save(update_fields=["name"])

        return series

    # 6. 만약 변경하려는 이름이 이미 내가 가진 다른 시리즈 이름과 겹친다면 (UniqueConstraint 위반)
    except IntegrityError:
        raise BaseCustomException(ErrorMessage.SERIES_ALREADY_EXISTS)


def delete_series(*, series_id: int, user: User) -> None:
    """본인의 시리즈를 삭제하는 서비스 로직입니다."""

    # 1. 전달받은 series_id와 user 정보로 삭제할 대상 시리즈를 조회합니다.
    series = Series.objects.filter(id=series_id, user=user).first()

    # 2. 대상 시리즈가 없다면 에러를 발생시켜 비정상적인 삭제 요청을 차단합니다.
    if not series:
        raise BaseCustomException(ErrorMessage.SERIES_SERVICE_PERMISSION)

    # 3. 권한이 확인되었으므로 시리즈를 데이터베이스에서 완전히 삭제(Hard Delete)합니다.
    series.delete()