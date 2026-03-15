import logging
from django.conf import settings
from google import genai
from google.genai import types

from apps.ai.prompts.tone_prompts import TONE_MAPPING
from apps.core.exceptions.base import BaseCustomException
from apps.core.exceptions.messages import ErrorMessage

# 현재 파일의 이름(__name__)을 기반으로 로거 인스턴스를 생성하여 로그를 추적하기 쉽게 함
logger = logging.getLogger(__name__)


def convert_text_tone(text: str, tone: str) -> str:  # type: ignore
    try:
        # 1. 클라이언트가 요청한 문체(tone)에 맞는 프롬프트를 찾습니다.
        system_prompt = TONE_MAPPING.get(tone)
        if not system_prompt:
            raise BaseCustomException(ErrorMessage.UNSUPPORTED_TONE)

        # 2. 새로운 google.genai의 Client 인스턴스를 생성하면서 환경변수(settings)의 API 키를 주입
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        # 3. GenerativeModel 인스턴스를 따로 만들지 않고, Client를 통해 바로 스트리밍 생성을 요청
        response = client.models.generate_content_stream(
            # 속도와 성능이 모두 뛰어난 최신의 gemini-2.5-flash 모델을 명시적으로 지정
            model="gemini-2.5-flash",
            # 사용자가 블로그 글로 변환하고자 하는 원본 텍스트를 전달
            contents=text,
            # 4. 모델의 지시사항, 온도 등의 세부 옵션은 GenerateContentConfig 객체에 묶어서 전달
            config=types.GenerateContentConfig(
                # 앞에서 찾은 시스템 프롬프트를 모델의 기본 지시사항으로 주입
                system_instruction=system_prompt,
                # 자연스럽고 적절한 변환을 위해 창의성 정도(온도)를 0.7로 설정
                temperature=0.7,
                # 블로그 글이 잘리지 않도록 넉넉하게 토큰 제한을 2500으로 제한
                max_output_tokens=2500,
            ),
        )

        # 5. 스트리밍 응답 객체(response)에서 생성되는 텍스트 조각(chunk)을 순회
        for chunk in response:
            # 조각 안에 텍스트 데이터가 정상적으로 존재하는지 확인
            if chunk.text:
                # 일반 문자열(String)이 아닌 UTF-8 바이트(Bytes)로 인코딩하여 반환
                # 장고가 내부적으로 문자를 처리하며 대기하는 시간을 없애줌
                yield chunk.text.encode("utf-8")

    # 우리가 위에서 직접 발생시킨 '지원하지 않는 문체' 에러를 잡음
    except ValueError as ve:
        # 서버 로그에 에러 원인을 기록함
        logger.error(f"잘못된 문체 요청: {ve}")
        # 이 에러를 API View로 다시 던져서 클라이언트에게 400 에러를 내려주도록 함
        raise

    # 그 외에 구글 서버 점검, 네트워크 단절 등 예측하지 못한 모든 에러를 잡음
    except Exception as e:
        # 원인을 파악할 수 있도록 상세한 에러를 로그에 남김
        logger.error(f"Gemini API 호출 중 오류 발생: {e}")
        # 유저에게는 내부 에러 상세 내용을 숨기고, 안전하고 친절한 메시지로 덮어씌워 던짐
        raise BaseCustomException(ErrorMessage.AI_CONVERSION_FAILED)
