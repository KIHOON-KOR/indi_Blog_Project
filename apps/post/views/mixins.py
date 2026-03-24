from rest_framework.response import Response


class PostListMixin:
    """게시글 목록 조회 시 반복되는 필터링 및 페이지네이션 로직을 분리한 믹스인 클래스입니다."""

    def get_filter_params(self, request):
        """요청(request)에서 쿼리 파라미터를 추출하고 정제하여 딕셔너리 형태로 반환합니다."""

        # 1. URL에서 '?series=숫자' 형태의 값을 문자열로 꺼내옴
        series_id_str = request.query_params.get("series")

        # 2. 값이 존재하고 숫자로만 이루어져 있다면 정수(int)로 변환하고, 아니라면 None을 할당
        series_id = (
            int(series_id_str) if series_id_str and series_id_str.isdigit() else None
        )

        # 3. URL에서 '?tag=문자열' 값을 꺼내옴 (태그 필터링용)
        tag_name = request.query_params.get("tag")

        # 4. URL에서 '?search=검색어' 값을 꺼내옴 (검색 기능용)
        search_keyword = request.query_params.get("search")

        # 5. 추출 및 정제된 파라미터들을 딕셔너리로 묶어서 반환
        # (서비스 레이어 함수 호출 시 **kwargs 형태로 깔끔하게 전달 가능)
        return {
            "series_id": series_id,
            "tag_name": tag_name,
            "search_keyword": search_keyword,
        }

    def get_paginated_response(self, queryset, serializer_class, request, context=None):
        """쿼리셋에 페이지네이션을 적용하고 DRF 규격에 맞는 Response 객체를 반환합니다."""

        # 1. 뷰(View) 클래스에 정의되어 있는 pagination_class를 기반으로 페이지네이터 인스턴스를 생성
        paginator = self.pagination_class()

        # 2. 전체 쿼리셋을 페이징 처리하여, 사용자가 요청한 현재 페이지에 해당하는 데이터만 잘라냄
        page = paginator.paginate_queryset(queryset, request, view=self)

        # 3. 페이징 처리가 성공적으로 이루어졌다면 (데이터가 방대하여 page 단위로 나뉘었다면)
        if page is not None:
            # 4. 잘라낸 페이지 데이터를 전달받은 시리얼라이저를 통해 직렬화 (필요시 context 포함)
            serializer = serializer_class(page, many=True, context=context)

            # 5. DRF의 페이지네이션 양식(count, next, previous, results)이 적용된 최종 응답을 반환
            return paginator.get_paginated_response(serializer.data)

        # 6. 만약 페이징 처리가 설정되지 않았거나 예외적으로 page가 None이라면, 전체 쿼리셋을 직렬화
        serializer = serializer_class(queryset, many=True, context=context)

        # 7. 직렬화된 전체 데이터를 일반 Response 객체로 감싸서 반환
        return Response(serializer.data)
