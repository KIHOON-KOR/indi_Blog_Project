from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.ai.serializers.tone_serializer import ToneConvertSerializer
from django.http import StreamingHttpResponse
from apps.ai.services.openai_service import convert_text_tone


class ToneConverterAPIView(APIView):
    # 무차별 요청(Rate Limiting) 방어를 위해 쓰로틀링 장착
    # settings.py의 DEFAULT_THROTTLE_RATES에 설정된 규칙(예: 분당 10회 등)을 따르게 됨
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        # 1. 시리얼라이저를 통한 엄격한 검증 (단순 딕셔너리 추출 대체)
        serializer = ToneConvertSerializer(data=request.data)

        # 2. 유효성 검사 실패 시 (글자 수 초과 등) 즉시 400 에러를 반환하여 AI 호출을 차단합니다.
        serializer.is_valid(raise_exception=True)

        # 3. 안전하게 검증이 끝난 데이터만 꺼내어 사용합니다.
        text = serializer.validated_data.get("text")
        tone = serializer.validated_data.get("tone")

        try:
            # Gemini 서비스 함수를 호출하여 결과를 받아옴
            converted_text = convert_text_tone(text=text, tone=tone)

            # 생성된 제너레이터를 StreamingHttpResponse에 담아 클라이언트에 반환함
            # content_type을 'text/plain' 혹은 'text/event-stream'으로 주어 텍스트 조각임을 알림
            response = StreamingHttpResponse(
                # 첫 번째 인자로 텍스트 조각들을 지속적으로 뿜어내는 제너레이터를 넣음
                converted_text,
                # content_type을 'text/event-stream'으로 변경하여 브라우저의 버퍼링을 원천 차단
                content_type="text/event-stream",
            )

            # 브라우저나 중간 프록시 서버가 이 응답을 캐싱(저장)하지 못하게 막음
            response["Cache-Control"] = "no-cache"
            # Nginx 같은 웹 서버를 사용할 경우, 버퍼링을 하지 말고 즉시 클라이언트로 쏘도록 지시
            response["X-Accel-Buffering"] = "no"

            return response

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
