import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from apps.core.exceptions.messages import ErrorMessage

logger = logging.getLogger("django")

def custom_exception_handler(exc, context):
    # 1. DRF 기본 핸들러 호출
    response = exception_handler(exc, context)

    # 2. 처리되지 않은 500 에러 처리
    if response is None:
        logger.error(f"[System Error] {exc}", exc_info=True) #
        return Response(
            {"error_detail": ErrorMessage.SYSTEM_ERROR.message, "code": ErrorMessage.SYSTEM_ERROR.code},
            status=ErrorMessage.SYSTEM_ERROR.status_code,
        )

    # 3. 응답 포맷 통일: {"error_detail": "...", "code": "...", "errors": {...}}
    custom_data = {
        "error_detail": response.data.get("detail", "유효하지 않은 요청입니다."),
        # BaseCustomException이면 코드가 들어가고, 아니면 "error"
        "code": getattr(exc, "default_code", "error")
    }

    # 유효성 검사(400) 실패 시 상세 정보 유지
    if response.status_code == 400 and "detail" not in response.data:
        custom_data["errors"] = response.data

    response.data = custom_data
    return response