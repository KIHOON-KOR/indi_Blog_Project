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
        # 클라이언트가 요청한 문체(tone)에 맞는 프롬프트를 찾습니다.
        system_prompt = TONE_MAPPING.get(tone)
        if not system_prompt:
            raise BaseCustomException(ErrorMessage.UNSUPPORTED_TONE)

        # Gemini 모델 인스턴스를 생성합니다.
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest", system_instruction=system_prompt
        )

        # 모델에게 실제 변환할 사용자의 텍스트를 전달하고 결과(응답)를 생성하도록 요청합니다.
        response = model.generate_content(
            text,  # 유저가 작성한 텍스트
            # 결과물 생성을 위한 세부 옵션을 설정합니다.
            generation_config=genai.types.GenerationConfig(
                # 0.7은 너무 뻔하지도, 너무 엉뚱하지도 않은 적절하고 자연스러운 문장을 만듬
                temperature=0.7,
                # 결과물이 너무 길어져서 토큰(비용)을 과다하게 쓰는 것을 방지
                max_output_tokens=1000,
            ),
        )

        # Gemini의 응답 객체에서 생성된 텍스트 문자열만 쏙 뽑아서 반환
        return response.text

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
