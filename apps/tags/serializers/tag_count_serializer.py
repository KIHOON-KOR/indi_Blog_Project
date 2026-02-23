from rest_framework import serializers
from apps.tags.models import Tag


class TagStatSerializer(serializers.ModelSerializer):
    """홈 화면 태그 클라우드용 시리얼라이저"""

    # annotate를 통해 동적으로 생성된 필드이므로 read_only=True로 선언
    post_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = ["id", "name", "post_count"]
