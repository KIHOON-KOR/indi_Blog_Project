import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response

from apps.core.exceptions.messages import ErrorMessage
from apps.core.exceptions.base import BaseCustomException

logger = logging.getLogger("django")


def custom_exception_handler(exc, context):
    # 1. DRF 기본 핸들러 호출
    response = exception_handler(exc, context)

    # 2. 처리되지 않은 500 에러 (서버 셧다운 방어)
    if response is None:
        logger.error(f"[System Error] {exc}", exc_info=True)
        return Response(
            {
                "code": ErrorMessage.SYSTEM_ERROR.code,
                "message": ErrorMessage.SYSTEM_ERROR.message,
            },
            status=ErrorMessage.SYSTEM_ERROR.status_code,
        )

    # 3. 응답 포맷 통일 로직 시작
    # 프론트엔드와 약속할 공통 뼈대: {"code": "...", "message": "..."}
    custom_data = {}

    if isinstance(exc, BaseCustomException):
        # 케이스 A: 우리가 ErrorMessage Enum으로 직접 정의하고 발생시킨 예외
        custom_data["code"] = exc.default_code
        custom_data["message"] = str(exc.detail)
    else:
        # 케이스 B: DRF 기본 내장 예외 (예: AuthenticationFailed, NotFound 등)
        custom_data["code"] = getattr(exc, "default_code", "error")

        # DRF 예외는 기본적으로 'detail'이라는 키에 메시지를 담아 보냅니다.
        if isinstance(response.data, dict) and "detail" in response.data:
            custom_data["message"] = str(response.data["detail"])
        else:
            custom_data["message"] = "유효하지 않은 요청입니다."

    # 4. Serializer Validation Error (400) 특화 처리
    # 사용자가 회원가입 등에서 입력값을 잘못 보냈을 때 (detail 키가 없고 필드명: [에러] 형태로 옴)
    if (
        response.status_code == 400
        and isinstance(response.data, dict)
        and "detail" not in response.data
    ):
        custom_data["code"] = ErrorMessage.INVALID_INPUT.code
        custom_data["message"] = ErrorMessage.INVALID_INPUT.message
        # 어느 필드가 틀렸는지 구체적인 이유를 'details'라는 키로 예쁘게 묶어서 보내줍니다.
        custom_data["details"] = response.data

        # 최종적으로 정제된 데이터를 응답 객체에 덮어씌웁니다.
    response.data = custom_data
    return response
