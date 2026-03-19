import requests
from django.conf import settings
import uuid
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from apps.user.models.social_account import SocialAccount

User = get_user_model()


def generate_unique_nickname(base_nickname: str) -> str:
    """
    소셜 로그인 시 중복되지 않는 닉네임을 생성하는 함수입니다.
    """
    # 1. 소셜 플랫폼에서 받아온 원본 닉네임을 초기값으로 설정
    nickname = base_nickname

    # 2. DB에 해당 닉네임이 이미 존재하는지 검사 (존재한다면 while 문 실행)
    while User.objects.filter(nickname=nickname).exists():
        # 3. 중복된다면, uuid를 이용해 랜덤한 4자리 영숫자를 생성
        random_str = uuid.uuid4().hex[:4]
        # 4. 원본 닉네임 뒤에 랜덤 문자열을 붙여 새로운 닉네임을 만듬 (예: myname_f1a2)
        nickname = f"{base_nickname}_{random_str}"

    # 5. 중복 검사를 통과한 고유한 닉네임을 반환
    return nickname


class GithubLoginService:
    # 메서드를 인스턴스화 없이 사용할 수 있도록 정적 메서드로 선언
    @staticmethod
    def github_login(code: str):
        # 1. 깃허브에서 Access Token을 받아오기 위한 URL
        token_req_url = "https://github.com/login/oauth/access_token"

        # 2. Access Token을 요청할 때 보낼 데이터(페이로드)를 구성
        data = {
            "client_id": settings.GITHUB_CLIENT_ID,  # 환경변수에 저장된 Client ID
            "client_secret": settings.GITHUB_CLIENT_SECRET,  # 환경변수에 저장된 Client Secret
            "code": code,  # 프론트엔드로부터 전달받은 인가 코드
        }

        # 3. 깃허브 API가 JSON 형태로 응답하도록 헤더를 설정
        headers = {"Accept": "application/json"}

        # 4. 깃허브 서버로 POST 요청을 보내 토큰을 발급받음
        token_req = requests.post(token_req_url, data=data, headers=headers)

        # 5. 응답받은 JSON 데이터에서 access_token 값만 추출
        token_json = token_req.json()
        error = token_json.get("error")

        # 6. 토큰 발급 중 에러가 발생했다면 예외를 발생시킴
        if error is not None:
            raise ValueError("GitHub 토큰을 받아오는데 실패했습니다.")

        access_token = token_json.get("access_token")

        # 7. 발급받은 토큰으로 깃허브 유저 정보를 요청할 URL
        user_req_url = "https://api.github.com/user"

        # 8. 토큰을 Authorization 헤더에 담아 GET 요청을 보냄
        user_req = requests.get(
            user_req_url, headers={"Authorization": f"Bearer {access_token}"}
        )

        # 9. 응답받은 유저 정보를 JSON 객체로 변환
        user_json = user_req.json()

        # 10. 깃허브의 유저 고유 ID와 아이디(login)를 가져옴
        github_id = str(user_json.get("id"))
        base_nickname = user_json.get("login")

        # 11. 깃허브 이메일이 비공개(null)로 올 경우를 대비하여 확실하게 처리함
        email = user_json.get("email")
        if not email:
            email = f"{github_id}@github.dummy.com"

        # 12. DB 작업 중 오류 발생 시 롤백하기 위해 트랜잭션 블록을 염
        with transaction.atomic():
            # 13. SocialAccount 테이블에서 깃허브 ID로 등록된 소셜 계정이 있는지 찾습니다.
            social_account = SocialAccount.objects.filter(
                provider="github", social_id=github_id
            ).first()

            # 14. 소셜 계정이 이미 존재한다면 (기존 가입 유저)
            if social_account:
                user = (
                    social_account.user
                )  # 해당 소셜 계정과 연결된 User 객체를 가져옵니다.

            # 15. 소셜 계정이 없다면 (신규 가입 유저)
            else:
                # 16. 혹시 같은 이메일로 가입한 기존 일반 유저가 있는지 확인
                user = User.objects.filter(email=email).first()  # type: ignore

                # 17. 일반 유저도 없다면 새로운 유저를 생성 (UserManager의 create_user 활용)
                if not user:
                    # 고유한 닉네임 생성
                    unique_nickname = generate_unique_nickname(base_nickname)

                    user = User.objects.create_user(
                        email=email,
                        nickname=unique_nickname,
                        password=None,  # 소셜 로그인이므로 비밀번호는 사용 불가 처리됨
                    )

                # 18. 새로 생성한(혹은 기존) 유저와 깃허브 ID를 연결하는 SocialAccount 레코드를 생성
                SocialAccount.objects.create(
                    user=user, provider="github", social_id=github_id
                )

        # 19. 유저 인증이 완료되었으므로, 프론트엔드에 전달할 자체 JWT 토큰을 생성
        refresh = RefreshToken.for_user(user)

        # 20. Access Token, Refresh Token, 그리고 유저 정보를 딕셔너리 형태로 반환
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": user,
        }


class DiscordLoginService:
    @staticmethod
    def discord_login(code: str, redirect_uri: str):
        # 1. 디스코드 토큰 발급 URL
        token_req_url = "https://discord.com/api/oauth2/token"

        # 2. 토큰 요청 페이로드 (디스코드는 grant_type과 redirect_uri가 필수)
        data = {
            "client_id": settings.DISCORD_CLIENT_ID,
            "client_secret": settings.DISCORD_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }

        # 3. 디스코드 API 권장 헤더 포맷
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # 4. 토큰 요청
        token_req = requests.post(token_req_url, data=data, headers=headers)
        token_json = token_req.json()

        if "error" in token_json:
            raise ValueError("Discord 토큰을 받아오는데 실패했습니다.")

        access_token = token_json.get("access_token")

        # 5. 유저 정보 요청 URL
        user_req_url = "https://discord.com/api/users/@me"
        user_req = requests.get(
            user_req_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        user_json = user_req.json()

        # 6. 유저 정보 추출 (디스코드는 id와 username, email을 반환)
        discord_id = str(user_json.get("id"))
        base_nickname = user_json.get("username")
        email = user_json.get("email")

        if not email:
            email = f"{discord_id}@discord.dummy.com"

        # 7. DB 트랜잭션
        with transaction.atomic():
            social_account = SocialAccount.objects.filter(
                provider="discord", social_id=discord_id
            ).first()

            if social_account:
                user = social_account.user
            else:
                user = User.objects.filter(email=email).first()  # type: ignore
                if not user:
                    unique_nickname = generate_unique_nickname(base_nickname)

                    user = User.objects.create_user(
                        email=email,
                        nickname=unique_nickname,
                        password=None,
                        is_email_verified=True,
                    )
                SocialAccount.objects.create(
                    user=user, provider="discord", social_id=discord_id
                )

        # 8. JWT 발급
        refresh = RefreshToken.for_user(user)

        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": user,
        }
