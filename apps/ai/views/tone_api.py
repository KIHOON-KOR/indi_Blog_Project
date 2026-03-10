from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.core.exceptions.base import BaseCustomException
from apps.core.exceptions.messages import ErrorMessage

from apps.ai.services.openai_service import convert_text_tone


class ToneConverterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # 클라이언트가 보낸 JSON 데이터 중 'text'를 가져옵니다.
        text = request.data.get("text")
        # 클라이언트가 보낸 JSON 데이터 중 'tone'을 가져옵니다.
        tone = request.data.get("tone")

        # 텍스트나 톤 중 하나라도 비어있다면 (유효성 검사 실패)
        if not text or not tone:
            raise BaseCustomException(ErrorMessage.INVALID_INPUT)

        try:
            # Gemini 서비스 함수를 호출하여 결과를 받아옴
            converted_text = convert_text_tone(text=text, tone=tone)

            # 에러 없이 무사히 변환되었다면, 200 성공 코드와 함께 변환된 텍스트를 돌려줌
            return Response(
                {"converted_text": converted_text}, status=status.HTTP_200_OK
            )

        # 지원하지 않는 문체 등 사용자의 잘못된 요청으로 인한 에러를 처리
        except ValueError as e:
            # 400 Bad Request와 함께 서비스 계층에서 던진 에러 메시지를 반환
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # 구글 API 서버 장애 등 백엔드 측의 예기치 않은 에러를 처리
        except RuntimeError as e:
            # 500 Internal Server Error와 함께 안전하게 포장된 에러 메시지를 반환
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
