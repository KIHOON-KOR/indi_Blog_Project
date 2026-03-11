import logging
from django.conf import settings
import google.generativeai as genai

from apps.ai.prompts.tone_prompts import TONE_MAPPING
from apps.core.exceptions.base import BaseCustomException
from apps.core.exceptions.messages import ErrorMessage


logger = logging.getLogger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)  # type: ignore


def convert_text_tone(text: str, tone: str) -> str:
    try:
        # 1. 클라이언트가 요청한 문체(tone)에 맞는 프롬프트를 찾습니다.
        system_prompt = TONE_MAPPING.get(tone)
        if not system_prompt:
            raise BaseCustomException(ErrorMessage.UNSUPPORTED_TONE)

        # 2. Gemini 모델 인스턴스를 생성합니다.
        model = genai.GenerativeModel(
            # 빠르고 가벼운 flash 모델을 사용
            model_name="gemini-flash-latest",
            # 앞에서 찾은 시스템 프롬프트를 모델의 기본 지시사항으로 주입
            system_instruction=system_prompt
        )

        # 3. 스트리밍 모드로 텍스트 생성 요청
        response = model.generate_content(
            # 변환할 원본 텍스트를 첫 번째 인자로 전달
            text,
            # 스트리밍 옵션을 켜서, 생성 즉시 응답을 받도록 설정
            stream=True,
            # 결과물 생성을 위한 세부 설정값을 전달
            generation_config=genai.types.GenerationConfig(
                # 자연스럽고 적절한 변환을 위해 창의성 정도(온도)를 0.7로 설정
                temperature=0.7,
                # 블로그 글이 잘리지 않도록 넉넉하게 토큰 제한을 2500으로 제한
                max_output_tokens=2500,
            ),
        )

        # 4. 스트리밍 응답 객체(response)에서 생성되는 텍스트 조각(chunk)을 순회
        for chunk in response:
            # 조각 안에 텍스트 데이터가 정상적으로 존재하는지 확인
            if chunk.text:
                # 일반 문자열(String)이 아닌 UTF-8 바이트(Bytes)로 인코딩하여 반환
                # 장고가 내부적으로 문자를 처리하며 대기하는 시간을 없애줌
                yield chunk.text.encode('utf-8')

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
