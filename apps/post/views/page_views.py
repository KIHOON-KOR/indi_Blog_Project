from django.shortcuts import render

def post_write_page(request):
    """게시글 작성 화면(HTML)을 렌더링합니다."""
    return render(request, 'post/write.html')