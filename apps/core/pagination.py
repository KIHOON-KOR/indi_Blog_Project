from typing import Any, Optional
from django.db.models import QuerySet
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response


class PostPageNumberPagination(PageNumberPagination):
    """
    프로젝트 전역에서 사용할 커스텀 페이지네이션 클래스입니다.
    페이지 범위를 벗어난 요청 시 에러 대신 빈 리스트를 반환하도록 설계되었습니다.
    """

    page_size = 10  # 기본 페이지 당 데이터 개수
    page_size_query_param = "size"  # 클라이언트가 size 파라미터로 개수 조절 가능
    max_page_size = 50  # 최대 페이지 당 데이터 개수 제한

    def paginate_queryset(
        self,
        queryset: QuerySet[Any],
        request: Request,
        view: Optional[APIView] = None,
    ) -> list[Any] | None:
        try:
            # DRF 기본 pagination 로직을 먼저 시도
            return super().paginate_queryset(queryset, request, view)

        # 페이지 번호가 결과 범위를 벗어났을 때(예: 데이터는 10개인데 2페이지 요청) 발생하는 예외를 잡음
        except NotFound:
            page_param = request.query_params.get(self.page_query_param, "1")

            # page 값 자체가 정수가 아닌 잘못된 형식인 경우 400 에러를 발생
            try:
                page_number = int(page_param)
            except (TypeError, ValueError):
                raise ValidationError("page는 정수여야 합니다.")

            # page가 0 이하인 경우도 유효하지 않은 요청으로 처리합니다.
            if page_number <= 0:
                raise ValidationError("page는 1 이상이어야 합니다.")

            # page_size를 가져오며 안전 처리를 수행합니다.
            page_size = self.get_page_size(request)
            if page_size is None:
                return list(queryset)

            # 장고의 기본 Paginator를 사용하여 메타데이터(총 개수 등)는 유지합니다.
            paginator = self.django_paginator_class(queryset, page_size)

            # 마지막 페이지 정보를 self.page에 설정하되, 반환할 데이터(object_list)만 비웁니다.
            # 이렇게 하면 프론트엔드에서 'count' 등은 제대로 받으면서 데이터만 빈 배열로 받게 됩니다.
            self.page = paginator.page(paginator.num_pages)
            self.page.object_list = []

            return []

    # DRF가 최종적으로 JSON 응답을 만들 때 호출하는 메서드입니다.
    def get_paginated_response(self, data):
        return Response(
            {
                # 전체 데이터의 개수를 보냅니다.
                "count": self.page.paginator.count,
                # 장고의 paginator가 이미 계산해둔 '총 페이지 수'를 프론트엔드로 보냅니다.
                "total_pages": self.page.paginator.num_pages,
                # 다음 페이지로 가는 API URL을 보냅니다.
                "next": self.get_next_link(),
                # 이전 페이지로 가는 API URL을 보냅니다.
                "previous": self.get_previous_link(),
                # 실제 게시글 데이터(리스트)를 보냅니다.
                "results": data,
            }
        )
