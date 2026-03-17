import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()


class PasswordResetService:
    """비밀번호 찾기 관련 비즈니스 로직 클래스"""

    @staticmethod
    def send_reset_code(email: str) -> None:
        """이메일을 받아 인증번호를 발송"""
        # 유저 존재 여부 및 소셜 계정 검증
        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError("가입되지 않은 이메일입니다.")

        # 유저가 일반 비밀번호가 없다면 (즉, 소셜 로그인 계정이라면)
        if not user.has_usable_password():
            raise ValidationError("소셜 로그인으로 가입된 계정입니다. 해당 소셜 플랫폼으로 로그인해주세요.")

        # 6자리 인증번호 생성 및 레디스 저장
        code = str(random.randint(100000, 999999))  # 무작위 6자리 숫자 생성
        cache_key = f"pwd_reset_{email}"  # 비밀번호 찾기 전용 캐시 방 이름 생성
        cache.set(cache_key, code, timeout=300)  # 레디스에 5분(300초) 동안 저장

        # 이메일 발송
        subject = "[블로그] 비밀번호 재설정 인증번호"  # 메일 제목
        message = f"비밀번호 재설정 인증번호는 {code} 입니다.\n5분 안에 입력하여 비밀번호를 변경해주세요."  # 메일 내용

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # 아까 설정해둔 '블로그 관리자 <이메일>' 주소
            [email],
            fail_silently=False,
        )

    @staticmethod
    def reset_password(email: str, code: str, new_password: str) -> None:
        """인증번호 확인 후 비밀번호를 실제 변경"""
        cache_key = f"pwd_reset_{email}"  # 레디스에서 꺼내올 방 이름
        saved_code = cache.get(cache_key)  # 저장된 인증번호 가져오기

        # 1. 인증번호 일치 여부 확인
        if not saved_code or saved_code != code:
            raise ValidationError("인증번호가 일치하지 않거나 만료되었습니다.")

        # 2. 비밀번호 변경 적용
        user = User.objects.filter(email=email).first()
        if user:
            # Django의 set_password 함수가 알아서 비밀번호를 안전하게 암호화
            user.set_password(new_password)
            # 변경된 비밀번호를 DB에 최종 저장(Commit)
            user.save()

        # 3. 보안 최적화(사용이 끝난 인증번호는 레디스에서 즉시 파기하여 재사용을 막음)
        cache.delete(cache_key)