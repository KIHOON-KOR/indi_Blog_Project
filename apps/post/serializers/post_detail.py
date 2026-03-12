from rest_framework import serializers
from apps.post.models import Post

GRADE_SETTINGS = [
    {"min": 500, "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/f2190a179021431f826762e0956a1902.png"},
    {"min": 300, "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/729bef20eaf546d89ee9342ea1ad83f0.png"},
    {"min": 200, "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/6d5199ad382648a285ed83f05a2bb1b2.png"},
    {"min": 150, "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/994bc8236ec1470bbf4bd4e1c3053b53.png"},
    {"min": 100, "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/d8fe986d15854aaa96fd8fb4ae5ad857.png"},
    {"min": 50,  "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/0e12672759274f2b8a63365cbc8c1c29.png"},
    {"min": 30,  "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/67dc5f4129464d359f4057e812aff476.png"},
    {"min": 10,  "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/033b3fb73deb40d496055712d87f1838.png"},
    {"min": 5,   "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/922009e1f1064d358fc41f265c119e0d.png"},
    {"min": 0,   "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/54be5c5e97fc4ce7a3129403f4dbf936.png"},
]


class PostDetailSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source="user.nickname", read_only=True)
    author_grade_image = serializers.SerializerMethodField()

    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")  # type: ignore
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()

    series_id = serializers.IntegerField(source="series.id", read_only=True)
    series_name = serializers.CharField(source="series.name", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "thumbnail",
            "author_nickname",
            "author_grade_image",
            "created_at",
            "visibility",
            "tags",
            "likes_count",
            "is_liked",
            "series_id",
            "series_name",
        ]

    # ✨ author_grade_image 필드의 값을 실제로 계산하는 메서드 (메서드명 규칙: get_ + 필드명)
    def get_author_grade_image(self, obj):
        # 1. 작성자(obj.user)가 지금까지 작성한 글 중에서 삭제되지 않은(deleted_at__isnull=True) 전체 글의 개수를 셉니다.
        total_count = Post.objects.filter(user=obj.user, deleted_at__isnull=True).count()

        # 2. GRADE_SETTINGS를 위에서부터 순회하며 개수(min) 조건을 충족하는 등급 이미지를 찾습니다.
        for grade in GRADE_SETTINGS:
            if total_count >= grade["min"]:
                return grade["imgUrl"]  # 조건을 만족하면 바로 해당 이미지 URL을 반환하고 종료합니다.

        # 3. 만약 매칭되는게 없다면 (혹시 모를 에러 방지용) 제일 기본 씨앗 이미지를 반환합니다.
        return GRADE_SETTINGS[-1]["imgUrl"]

    def get_is_liked(self, obj) -> bool:
        # 1. 뷰(View)에서 넘겨준 context 안에서 현재 요청(request) 객체를 가져옵니다.
        request = self.context.get("request")

        # 2. 요청 객체가 존재하고, 로그인된 사용자(is_authenticated)일 경우에만 검사합니다.
        if request and request.user.is_authenticated:
            # 3. 현재 게시글(obj)의 좋아요(likes) 목록 중에 현재 로그인한 유저가 있는지(exists) 확인하여 True/False를 반환합니다.
            return obj.likes.filter(user=request.user).exists()

        # 4. 로그인하지 않은 사용자라면 무조건 False(좋아요 안 누름)를 반환합니다.
        return False
