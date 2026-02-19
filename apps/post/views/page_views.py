from django.shortcuts import render


def post_write_page(request):
    """게시글 작성 화면(HTML)을 렌더링합니다."""
    return render(request, "post/write.html")


def my_post_list_page(request):
    """내 블로그(내가 쓴 공개글) 화면을 렌더링합니다."""
    return render(request, "post/my_list.html")


def global_post_list_page(request):
    """전체 피드(모든 사용자의 공개글) 화면을 렌더링합니다."""
    return render(request, "post/global_list.html")


def temp_post_list_page(request):
    """임시 저장글 관리 화면을 렌더링합니다."""
    return render(request, "post/temp_list.html")
