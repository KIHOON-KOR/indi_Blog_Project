from django.shortcuts import render

def series_my_list_page(request):
    """내 시리즈 관리 페이지 렌더링"""
    return render(request, "series/my_list.html")

def series_detail_page(request, series_id):
    """특정 시리즈의 게시글 목록 페이지 렌더링"""
    return render(request, "series/detail.html")