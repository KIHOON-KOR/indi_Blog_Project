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


class PostDetailSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source="user.nickname", read_only=True)
    author_profile_image = serializers.CharField(
        source="user.profile_img", read_only=True
    )
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
            "author_profile_image",
            "author_grade_image",
            "created_at",
            "visibility",
            "tags",
            "likes_count",
            "is_liked",
            "series_id",
            "series_name",
        ]

    def get_author_grade_image(self, obj):
        # DB에서 미리 계산해준 'author_total_posts' 값을 바로 사용(쿼리 낭비 X)
        total_count = getattr(obj, "author_total_posts", 0)

        # 미리 정의된 GRADE_SETTINGS를 순회하며 조건 검사
        for grade in GRADE_SETTINGS:
            if total_count >= grade["min"]:
                return grade["imgUrl"]

        return GRADE_SETTINGS[-1]["imgUrl"]

    def get_is_liked(self, obj) -> bool:
        # Service에서 Exists 서브쿼리를 통해 True/False 값을 'is_liked_by_user'로 붙여주기
        # DB를 찌르지 않고 해당 값을 가져오기만 함 (비로그인 상태이거나 값이 없으면 기본값 False 반환)
        return getattr(obj, "is_liked_by_user", False)
