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
