from rest_framework import serializers
from apps.series.models import Series


class SeriesCreateSerializer(serializers.ModelSerializer):
    """시리즈 생성을 위한 시리얼라이저입니다."""

    class Meta:
        model = Series
        fields = ["name"]


class SeriesListSerializer(serializers.ModelSerializer):
    """시리즈 목록 조회를 위한 시리얼라이저입니다."""

    class Meta:
        model = Series
        fields = ["id", "name", "created_at", "updated_at"]
