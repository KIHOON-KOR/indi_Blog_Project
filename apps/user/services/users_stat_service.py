from apps.post.models import Post

# 등급 설정(GRADE_SETTINGS)
GRADE_SETTINGS = [
    {"min": 500, "label": "울창한 생명의 숲", "msg": "수많은 이야기가 모여 전설적인 숲을 이루었습니다!", "level": 9,
     "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/f2190a179021431f826762e0956a1902.png",
     "cssClass": "grade-icon-lv9"},
    {"min": 300, "label": "웅장한 고목", "msg": "깊은 뿌리를 내린 든든한 고목이 되었습니다.", "level": 8,
     "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/729bef20eaf546d89ee9342ea1ad83f0.png",
     "cssClass": "grade-icon-lv8"},
    {"min": 200, "label": "탐스러운 열매 나무", "msg": "그동안의 노력이 달콤한 열매로 맺혔어요.", "level": 7,
     "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/6d5199ad382648a285ed83f05a2bb1b2.png",
     "cssClass": "grade-icon-lv7"},
    {"min": 150, "label": "만개한 꽃나무", "msg": "가지마다 아름다운 꽃이 활짝 피어났습니다.", "level": 6,
     "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/994bc8236ec1470bbf4bd4e1c3053b53.png",
     "cssClass": "grade-icon-lv6"},
    {"min": 100, "label": "풍성한 나무", "msg": "잎사귀가 아주 풍성하게 열린 듬직한 나무입니다!", "level": 5,
     "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/d8fe986d15854aaa96fd8fb4ae5ad857.png",
     "cssClass": "grade-icon-lv5"},
    {"min": 50, "label": "작은 나무", "msg": "이제 어엿한 나무의 모습을 갖추었네요.", "level": 4,
     "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/0e12672759274f2b8a63365cbc8c1c29.png",
     "cssClass": "grade-icon-lv4"},
    {"min": 30, "label": "튼튼한 묘목", "msg": "비바람에도 흔들리지 않는 튼튼한 줄기가 생겼어요.", "level": 3,
     "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/67dc5f4129464d359f4057e812aff476.png",
     "cssClass": "grade-icon-lv3"},
    {"min": 10, "label": "어린 묘목", "msg": "새로운 잎사귀들이 힘차게 돋아나고 있습니다.", "level": 2,
     "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/033b3fb73deb40d496055712d87f1838.png",
     "cssClass": "grade-icon-lv2"},
    {"min": 5, "label": "파릇한 새싹", "msg": "흙을 뚫고 예쁜 줄기가 올라왔어요!", "level": 1,
     "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/922009e1f1064d358fc41f265c119e0d.png",
     "cssClass": "grade-icon-lv1"},
    {"min": 0, "label": "희망찬 씨앗", "msg": "첫 글을 작성해서 씨앗을 틔워주세요.", "level": 0,
     "imgUrl": "https://hoon-blog-uploader-0112.s3.ap-northeast-2.amazonaws.com/post/thumbnails/2026/03/11/54be5c5e97fc4ce7a3129403f4dbf936.png",
     "cssClass": "grade-icon-lv0"},
]


def get_user_garden_stats(user):
    """
    특정 유저의 정원(잔디밭 및 등급) 통계 데이터를 계산하여 반환하는 서비스 함수
    """

    # 1. DB 조회: 해당 유저의 정상 발행된 글을 가져오고 총 개수를 구함
    user_posts = Post.objects.filter(author=user, is_temp=False)
    total_count = user_posts.count()

    # 2. 날짜 추출: 히트맵을 위해 날짜(created_at)만 뽑아내어 리스트로 만듬 (본문 데이터 배제)
    post_dates = list(user_posts.values_list('created_at__date', flat=True))

    # 3. 날짜 포맷팅: 프론트엔드에서 사용하기 쉽게 'YYYY-M-D' 문자열로 변환
    formatted_dates = [
        date.strftime('%Y-%-m-%-d') if hasattr(date, 'strftime') else str(date)
        for date in post_dates
    ]

    # 4. 현재 등급 계산: 내 글 개수를 만족하는 가장 높은 등급을 찾기
    current_grade = next(
        (g for g in GRADE_SETTINGS if total_count >= g["min"]),
        GRADE_SETTINGS[-1]
    )

    # 5. 다음 등급 계산: GRADE_SETTINGS를 역순으로 순회하여 남은 목표 등급 찾기
    reversed_settings = list(reversed(GRADE_SETTINGS))
    next_grade = next(
        (g for g in reversed_settings if g["min"] > total_count),
        None
    )

    # 6. 진행률 계산 초기화: 기본값은 만렙(100%)과 남은 글 수 0으로 설정
    progress_percent = 100
    remain_posts = 0

    # 7. 진행률 수학적 계산: 만렙이 아닐 경우 퍼센티지와 남은 개수를 계산
    if next_grade:
        remain_posts = next_grade["min"] - total_count
        required_for_next = next_grade["min"] - current_grade["min"]
        earned_in_current = total_count - current_grade["min"]

        # ZeroDivisionError를 방지 및 정확한 퍼센트를 산출
        if required_for_next > 0:
            progress_percent = (earned_in_current / required_for_next) * 100

    # 8. 계산된 모든 데이터를 딕셔너리 형태로 반환 (JSON 직렬화 가능 형태)
    return {
        "total_count": total_count,
        "current_grade": current_grade,
        "next_grade": next_grade,
        "progress_percent": progress_percent,
        "remain_posts": remain_posts,
        "heatmap_dates": formatted_dates
    }