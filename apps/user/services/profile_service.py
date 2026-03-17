from apps.user.models import User
from apps.user.services.users_stat_service import get_user_garden_stats
from apps.core.exceptions.base import BaseCustomException
from apps.core.exceptions.messages import ErrorMessage


def get_public_profile(nickname: str) -> dict:
    """
    닉네임을 기반으로 유저를 찾아 공개용 프로필 데이터를 조립해 반환하는 서비스 함수입니다.
    """
    # 1. DB 조회 시도
    try:
        # 전달받은 닉네임과 정확히 일치하는 단일 유저 객체를 가져옴
        target_user = User.objects.get(nickname=nickname)
    except User.DoesNotExist:
        raise BaseCustomException(ErrorMessage.USER_NOT_FOUND)

    # 2. 찾은 유저 객체를 기존 통계 서비스 함수에 넘겨 활동 통계 데이터(게시글 수, 등급 등)를 가져옴
    stats_data = get_user_garden_stats(target_user)

    # 3. View와 Serializer로 전달할 최종 데이터를 딕셔너리 형태로 조립해 반환
    return {
        "user_info": {
            "nickname": target_user.nickname,  # 유저의 닉네임
            "profile_img": target_user.profile_img,  # 유저의 프로필 이미지 URL
            "bio": target_user.bio,  # 유저의 한줄 자기소개
        },
        "stats": {
            "total_post_count": stats_data["total_count"],  # 총 작성 게시물 수
            "current_grade": stats_data["current_grade"],  # 현재 등급
            "next_grade": stats_data["next_grade"],  # 다음 등급
            "progress_percent": stats_data[
                "progress_percent"
            ],  # 다음 등급까지의 퍼센트
        },
    }


def check_nickname_available(current_user, nickname: str) -> tuple[bool, str]:
    """
    닉네임 중복 여부를 검사하고 (사용가능여부_Boolean, 메시지_String) 형태의 튜플로 반환합니다.
    """

    # 1. 사용자가 입력한 닉네임이 자신의 현재 닉네임과 완전히 똑같은 경우
    if current_user.nickname == nickname:
        return True, "현재 사용 중인 닉네임입니다."

    # 2. DB의 User 테이블에서 입력받은 닉네임과 일치하는 데이터가 존재하는지(exists) 확인
    is_exist = User.objects.filter(nickname=nickname).exists()

    # 3. 만약 이미 누군가 사용 중인 닉네임이라면
    if is_exist:
        return False, "이미 사용 중인 닉네임입니다."

    # 4. 위의 두 조건에 모두 걸리지 않았다면 완전히 새로운 닉네임이므로
    return True, "사용 가능한 닉네임입니다."