from rest_framework import serializers


class ToneConvertSerializer(serializers.Serializer):
    """
    텍스트 변환 API의 입력값을 검증하는 시리얼라이저입니다.
    """

    text = serializers.CharField(
        max_length=2000,  # 외부 LLM 비용 폭증을 막기 위해 2000자로 길이를 제한
        required=True,
        error_messages={
            "required": "변환할 텍스트를 입력해주세요.",
            "max_length": "텍스트는 최대 2000자까지 변환 가능합니다.",  # 에러 메시지
        },
    )
    tone = serializers.CharField(
        required=True, error_messages={"required": "원하시는 문체를 선택해주세요."}
    )
