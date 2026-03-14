from django.shortcuts import render


def login_page(request):
    """로그인 화면(HTML)을 렌더링합니다."""
    return render(request, "user/login.html")


def signup_page(request):
    """회원가입 화면(HTML)을 렌더링합니다."""
    return render(request, "user/signup.html")


def mypage_view(request):
    """마이페이지 화면(HTML)을 렌더링합니다."""
    return render(request, "user/mypage.html")


def public_profile_page(request, nickname):
    """
    타인의 공개 프로필 화면(HTML)을 렌더링하는 함수입니다.
    """
    # templates/user/public_profile.html 파일을 렌더링하며,
    # 템플릿 변수로 닉네임을 넘겨줍니다.
    return render(request, "user/public_profile.html", {"nickname": nickname})
