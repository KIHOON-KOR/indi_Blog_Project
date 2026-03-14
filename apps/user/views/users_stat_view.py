from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.user.services.users_stat_service import get_user_garden_stats


class UserGardenStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. 서비스 레이어 호출(통계데이터 받아오기)
        stats_data = get_user_garden_stats(request.user)

        # 2. 받아온 딕셔너리 데이터를 JSON 형태로 클라이언트에 응답
        return Response(stats_data)