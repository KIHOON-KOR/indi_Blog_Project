from django.shortcuts import render


def home(request):
    """메인 홈페이지(HTML)를 렌더링합니다."""
    return render(request, "home.html")
