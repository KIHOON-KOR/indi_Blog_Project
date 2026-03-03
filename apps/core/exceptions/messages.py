from enum import Enum
from rest_framework import status


class ErrorMessage(Enum):
    """
    프로젝트 전체 에러 메시지 정의
    """

    # --- 공통 에러 ---
    SYSTEM_ERROR = (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "server_error",
        "서버 내부 오류가 발생했습니다.",
    )
    INVALID_INPUT = (
        status.HTTP_400_BAD_REQUEST,
        "invalid_input",
        "유효하지 않은 입력값입니다.",
    )
    PERMISSION_DENIED = (
        status.HTTP_403_FORBIDDEN,
        "permission_denied",
        "권한이 없습니다.",
    )
    NOT_FOUND = (
        status.HTTP_404_NOT_FOUND,
        "not_found",
        "요청한 리소스를 찾을 수 없습니다.",
    )

    # --- 유저(User) 관련 ---
    EMAIL_ALREADY_EXISTS = (
        status.HTTP_400_BAD_REQUEST,
        "email_exists",
        "이미 존재하는 이메일입니다.",
    )
    LOGIN_FAILED = (
        status.HTTP_401_UNAUTHORIZED,
        "login_failed",
        "이메일 또는 비밀번호가 일치하지 않습니다.",
    )
    USER_INACTIVE = (
        status.HTTP_403_FORBIDDEN,
        "user_inactive",
        "해당 계정은 비활성화 상태입니다.",
    )
    EMAIL_REQUIRED = (
        status.HTTP_400_BAD_REQUEST,
        "email_required",
        "이메일은 필수 입력값입니다.",
    )

    # --- 포스트/댓글/시리즈 관련  ---
    POST_NOT_FOUND = (
        status.HTTP_404_NOT_FOUND,
        "post_not_found",
        "존재하지 않는 게시글입니다.",
    )
    COMMENT_NOT_FOUND = (
        status.HTTP_404_NOT_FOUND,
        "comment_not_found",
        "존재하지 않는 댓글입니다.",
    )
    NOT_POST_AUTHOR = (
        status.HTTP_403_FORBIDDEN,
        "not_post_author",
        "게시글 수정/삭제 권한이 없습니다.",
    )
    NOT_COMMENT_AUTHOR = (
        status.HTTP_403_FORBIDDEN,
        "not_comment_author",
        "댓글 수정/삭제 권한이 없습니다.",
    )
    SERIES_ALREADY_EXISTS = (
        status.HTTP_400_BAD_REQUEST,
        "series_already_exists",
        "이미 존재하는 시리즈 이름입니다.",
    )
    SERIES_PERMISSION_DENIED = (
        status.HTTP_403_FORBIDDEN,
        "series_permission_denied",
        "자신의 시리즈에만 게시글을 추가할 수 있습니다.",
    )

    @property
    def status_code(self):
        return self.value[0]

    @property
    def code(self):
        return self.value[1]

    @property
    def message(self):
        return self.value[2]
