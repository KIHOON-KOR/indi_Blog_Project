from rest_framework import serializers
from apps.post.models import Post

GRADE_SETTINGS = [
    {
        "min": 500,
        "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/f2190a179021431f826762e0956a1902.png",
    },
    {
        "min": 300,
        "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/729bef20eaf546d89ee9342ea1ad83f0.png",
    },
    {
        "min": 200,
        "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/6d5199ad382648a285ed83f05a2bb1b2.png",
    },
    {
        "min": 150,
        "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/994bc8236ec1470bbf4bd4e1c3053b53.png",
    },
    {
        "min": 100,
        "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/d8fe986d15854aaa96fd8fb4ae5ad857.png",
    },
    {
        "min": 50,
        "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/0e12672759274f2b8a63365cbc8c1c29.png",
    },
    {
        "min": 30,
        "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/67dc5f4129464d359f4057e812aff476.png",
    },
    {
        "min": 10,
        "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/033b3fb73deb40d496055712d87f1838.png",
    },
    {
        "min": 5,
        "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/922009e1f1064d358fc41f265c119e0d.png",
    },
    {
        "min": 0,
        "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/54be5c5e97fc4ce7a3129403f4dbf936.png",
    },
]


class PostListSerializer(serializers.ModelSerializer):
    """목록 조회를 위한 시리얼라이저"""

    author_nickname = serializers.CharField(source="user.nickname", read_only=True)
    author_profile_image = serializers.CharField(
        source="user.profile_img", read_only=True
    )
    author_grade_image = serializers.SerializerMethodField()

    likes_count = serializers.IntegerField(read_only=True)
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")  # type: ignore

    series_id = serializers.IntegerField(source="series.id", read_only=True)
    series_name = serializers.CharField(source="series.name", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "summary",
            "thumbnail",
            "author_nickname",
            "author_profile_image",
            "author_grade_image",
            "created_at",
            "visibility",
            "likes_count",
            "tags",
            "series_id",
            "series_name",
        ]

    # 1. 시리얼라이저가 실행될 때 유저별 글 개수를 기억할 딕셔너리 준비
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._author_counts = {}

    # 2. 등급 이미지 URL을 계산하는 메서드 최적화
    def get_author_grade_image(self, obj):
        user_id = obj.user_id

        # 만약 이 유저의 글 개수를 아직 계산한 적이 없다면? -> 딱 1번만 DB에서 카운트 쿼리 실행
        if user_id not in self._author_counts:
            self._author_counts[user_id] = Post.objects.filter(
                user_id=user_id,
                deleted_at__isnull=True  # (꿀팁) 기존 코드에 휴지통에 간 글을 제외하는 로직이 빠져있어서 추가했습니다!
            ).count()

        # 이미 계산된 유저라면 쿼리 없이 딕셔너리에서 바로 꺼내옴 (N+1 방어)
        total_count = self._author_counts[user_id]

        for grade in GRADE_SETTINGS:
            if total_count >= grade["min"]:
                return grade["imgUrl"]

        return GRADE_SETTINGS[-1]["imgUrl"]
