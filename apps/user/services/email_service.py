import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings


class EmailVerificationService:
    """이메일 인증 관련 핵심 로직들을 모아둔 서비스 클래스"""

    @staticmethod
    def send_verification_code(email: str) -> None:
        """이메일 주소를 넘겨받아 인증번호를 발송하는 함수"""
        # 100000부터 999999 사이의 무작위 숫자를 생성해 문자열로 만듬
        code = str(random.randint(100000, 999999))

        # 이 유저만의 고유한 캐시 방 이름(키)을 생성 (예: email_code_abc@abc.com)
        cache_key = f"email_code_{email}"
        # 생성한 방 이름에 인증번호를 저장하고, 300초(5분) 뒤에 자동 폭파되게 설정
        cache.set(cache_key, code, timeout=300)

        # 사용자 메일함에 표시될 이메일의 제목
        subject = "[블로그] 회원가입 이메일 인증번호"
        # 사용자에게 보여질 이메일의 본문 내용
        message = f"인증번호는 {code} 입니다.\n5분 안에 입력해주세요."

        # 실제로 이메일 발송 작업을 실행
        send_mail(
            subject,  # 메일 제목
            message,  # 메일 본문
            settings.DEFAULT_FROM_EMAIL,  # 보내는 사람 (settings.py 기준)
            [email],  # 받는 사람 (사용자가 입력한 이메일 주소를 리스트에 담음)
            # 메일 발송에 실패하면 서버가 에러를 내뱉도록 하여 문제를 빨리 파악하게 함
            fail_silently=False,
        )

    @staticmethod
    def verify_code(email: str, code: str) -> bool:
        """이메일과 사용자가 입력한 번호를 받아 맞는지 검사"""
        # 저장할 때 썼던 것과 똑같은 캐시 방 이름을 생성
        cache_key = f"email_code_{email}"
        # 해당 방 이름으로 캐시를 뒤져서 저장된 인증번호를 꺼내옴
        saved_code = cache.get(cache_key)

        # 저장된 번호가 존재하고(5분 안 지남), 사용자가 입력한 번호와 똑같다면
        if saved_code and saved_code == code:
            # 인증이 끝났으므로 보안을 위해 사용된 인증번호 캐시를 즉시 지움
            cache.delete(cache_key)

            # 인증을 통과했다는 것을 증명하기 위한 새로운 캐시 방 이름을 만듬
            verified_key = f"email_verified_{email}"
            # 회원가입을 마칠 때까지 여유를 주기 위해 1800초(30분) 동안 '인증됨(True)' 딱지를 붙여둠
            cache.set(verified_key, True, timeout=1800)
            return True

        return False
