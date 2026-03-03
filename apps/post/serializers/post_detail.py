from rest_framework import serializers
from apps.post.models import Post


class PostDetailSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source="user.nickname", read_only=True)

    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")  # type: ignore
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "thumbnail",
            "author_nickname",
            "created_at",
            "visibility",
            "tags",
            "likes_count",
            "is_liked",
            "series",
        ]

    def get_is_liked(self, obj) -> bool:
        # 1. 뷰(View)에서 넘겨준 context 안에서 현재 요청(request) 객체를 가져옵니다.
        request = self.context.get("request")

        # 2. 요청 객체가 존재하고, 로그인된 사용자(is_authenticated)일 경우에만 검사합니다.
        if request and request.user.is_authenticated:
            # 3. 현재 게시글(obj)의 좋아요(likes) 목록 중에 현재 로그인한 유저가 있는지(exists) 확인하여 True/False를 반환합니다.
            return obj.likes.filter(user=request.user).exists()

        # 4. 로그인하지 않은 사용자라면 무조건 False(좋아요 안 누름)를 반환합니다.
        return False
