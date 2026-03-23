import logging
import json
from django.conf import settings
from google import genai
from google.genai import types

from apps.ai.prompts.tone_prompts import TONE_MAPPING
from apps.core.exceptions.messages import ErrorMessage
from apps.core.exceptions.base import BaseCustomException

logger = logging.getLogger(__name__)

# SDK Client 인스턴스 전역(Global) 재사용
# 파일이 로드될 때 한 번만 인스턴스를 생성하므로, 매 요청마다 발생하는 연결 초기화 비용(오버헤드)을 줄임
try:
    # 1. 새로운 google.genai의 Client 인스턴스를 생성하면서 환경변수(settings)의 API 키를 주입
    gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
except Exception as e:
    logger.error(f"Gemini Client 초기화 실패: {e}")
    gemini_client = None  # 환경변수 문제 등으로 실패할 경우를 대비한 방어 로직


def convert_text_tone(text: str, tone: str):
    try:
        # 2. 클라이언트가 요청한 문체(tone)에 맞는 프롬프트를 찾습니다.
        system_prompt = TONE_MAPPING.get(tone)
        if not system_prompt:
            raise BaseCustomException(ErrorMessage.UNSUPPORTED_TONE)

        # 3. 클라이언트 초기화가 모종의 이유로 실패했다면 여기서 막음
        if not gemini_client:
            raise RuntimeError("AI 클라이언트를 초기화할 수 없습니다.")

        # 4. 매번 새로 만들던 client 대신, 글로벌 영역에 띄워둔 gemini_client를 재사용
        response = gemini_client.models.generate_content_stream(
            # 속도와 성능이 모두 뛰어난 최신의 gemini-2.5-flash 모델을 명시적으로 지정
            model="gemini-2.5-flash",
            # 사용자가 블로그 글로 변환하고자 하는 원본 텍스트를 전달
            contents=text,
            # 5. 모델의 지시사항, 온도 등의 세부 옵션은 GenerateContentConfig 객체에 묶어서 전달
            config=types.GenerateContentConfig(
                # 앞에서 찾은 시스템 프롬프트를 모델의 기본 지시사항으로 주입
                system_instruction=system_prompt,
                # 자연스럽고 적절한 변환을 위해 창의성 정도(온도)를 0.7로 설정
                temperature=0.7,
                # 블로그 글이 잘리지 않도록 넉넉하게 토큰 제한을 2500으로 제한
                max_output_tokens=2500,
            ),
        )

        # 6. 스트리밍 응답 객체(response)에서 생성되는 텍스트 조각(chunk)을 순회
        for chunk in response:
            if chunk.text:
                # 순수 텍스트 대신 SSE(Server-Sent Events) 표준 포맷으로 변환
                # 줄바꿈(\n) 등의 문자가 깨지지 않도록 json.dumps를 사용하여 텍스트를 감쌈
                sse_payload = json.dumps({"text": chunk.text}, ensure_ascii=False)

                # SSE 포맷 규약에 맞게 'data: {payload}\n\n' 형태로 만들어서 내보냅니다.
                yield f"data: {sse_payload}\n\n".encode("utf-8")

    # 제너레이터 실행 도중(이미 200 OK로 스트리밍이 진행되는 도중) 구글 API 등에 장애가 발생했다면
    except Exception as e:
        logger.error(f"Gemini API 스트리밍 중 오류 발생: {e}")

        # HTTP 상태 코드를 500으로 바꿀 수는 없지만, 프론트엔드가 에러임을 알 수 있게
        # event: error 라는 커스텀 이벤트를 발생시켜 에러 메시지를 보냄
        error_payload = json.dumps({"error": "AI 텍스트 생성 중 일시적인 서버 오류가 발생했습니다."}, ensure_ascii=False)

        # 프론트엔드는 이 형태를 받으면 정상 데이터 처리를 멈추고 에러 팝업을 띄울 수 있습니다.
        yield f"event: error\ndata: {error_payload}\n\n".encode("utf-8")