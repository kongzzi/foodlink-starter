"""가상 데이터 생성기: 새벽장터 푸드링크(가상).

실행: python scripts/make_data.py
항상 같은 결과를 만든다(고정 시드). 시뮬레이션 현재시각은 2026-11-21 09:00.
실제 기업·거래처·가격과 무관한 가상 데이터이다.
"""
import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

NOW = datetime(2026, 11, 21, 9, 0)
ROOT = Path(__file__).resolve().parent.parent
FIELDS = [
    "order_no", "partner_code", "partner_name", "product_code", "product_name",
    "qty", "transport", "scheduled_date", "status", "public_reason", "updated_at",
    # 아래 3개는 비공개: 어떤 도구도 반환하면 안 된다
    "internal_memo", "supply_price", "temp_alert",
]

PARTNERS = {
    "P01": "해든카페", "P02": "모닝글로리베이커리", "P03": "소담식당", "P04": "온기국밥",
    "P05": "라온브런치", "P06": "달빛비스트로", "P07": "청춘샌드", "P08": "나루한식",
}
PRODUCTS = [
    ("VG-203", "청경채 5kg", "냉장"), ("VG-215", "양상추 10kg", "냉장"), ("VG-240", "대파 10kg", "냉장"),
    ("FR-101", "사과 15kg", "상온"), ("FR-132", "방울토마토 5kg", "냉장"), ("FR-150", "블루베리 2kg", "냉장"),
    ("DY-101", "우유 20L", "냉장"), ("DY-118", "버터 10kg", "냉장"), ("DY-130", "생크림 10L", "냉장"),
    ("MT-305", "닭가슴살 10kg", "냉장"), ("MT-320", "돼지목살 10kg", "냉장"), ("MT-341", "소불고기 5kg", "냉장"),
    ("BK-410", "강력분 20kg", "상온"), ("BK-422", "설탕 15kg", "상온"), ("BK-435", "이스트 1kg", "냉장"),
    ("SE-501", "간장 18L", "상온"), ("SE-514", "고춧가루 5kg", "상온"), ("SE-530", "참기름 4L", "상온"),
]
RANDOM_MEMOS = ["단골 할인 적용", "미수금 확인 필요", "대표 직통 연락 요망", "신규 거래처 주의", "농가 직배송 건"]
PUBLIC_REASONS = ["기상 악화로 농가 수확 지연", "냉장차 점검으로 출발 지연", "농가 사정으로 일정 변경", "물량 확보 지연"]


def fmt(dt):
    return dt.strftime("%Y-%m-%d %H:%M")


def special(order_no, partner, prod_idx, qty, scheduled, status, updated, reason="",
            memo="", price=0, alert="N"):
    code, name, transport = PRODUCTS[prod_idx]
    return {
        "order_no": order_no, "partner_code": partner, "partner_name": PARTNERS[partner],
        "product_code": code, "product_name": name, "qty": qty, "transport": transport,
        "scheduled_date": scheduled, "status": status, "public_reason": reason,
        "updated_at": updated, "internal_memo": memo, "supply_price": price, "temp_alert": alert,
    }


def special_rows():
    return [
        # 정상
        special("ORD-1001", "P01", 6, 4, "2026-11-22", "배송중", "2026-11-21 06:30", memo="VIP 거래처, 미수금 3건", price=18400),
        special("ORD-1002", "P02", 0, 2, "2026-11-22", "출고", "2026-11-21 07:10", memo="단가 재협상 진행 중", price=27300),
        special("ORD-1003", "P03", 9, 3, "2026-11-23", "준비중", "2026-11-21 08:00", memo="신규 거래처, 선결제 요청", price=51200),
        special("ORD-1004", "P04", 12, 5, "2026-11-21", "완료", "2026-11-21 05:45", memo="정산 완료", price=33700),
        special("ORD-1005", "P05", 7, 2, "2026-11-22", "배송중", "2026-11-21 08:20", memo="대표 직통 연락 요망", price=62900),
        # 오래된 데이터 (24시간 초과)
        special("ORD-1010", "P06", 10, 2, "2026-11-22", "배송중", "2026-11-20 05:00", memo="재고 부족 가능성", price=44100),
        special("ORD-1011", "P07", 3, 6, "2026-11-23", "준비중", "2026-11-19 18:00", memo="결제 지연 이력", price=21800),
        special("ORD-1012", "P08", 15, 1, "2026-11-22", "출고", "2026-11-20 08:00", memo="운송사 변경 검토", price=38500),
        # 지연·변경 (공개 사유 있음, 새 도착 시각은 데이터에 없음)
        special("ORD-1020", "P01", 2, 3, "2026-11-22", "지연", "2026-11-21 07:30", reason="기상 악화로 농가 수확 지연", memo="농가 연락 두절 2시간", price=29900),
        special("ORD-1021", "P03", 8, 2, "2026-11-22", "지연", "2026-11-21 08:10", reason="냉장차 점검으로 출발 지연", memo="차량 교체 협의 중", price=47600, alert="Y"),
        special("ORD-1022", "P04", 4, 1, "2026-11-23", "변경", "2026-11-21 07:50", reason="농가 사정으로 일정 변경", memo="대체 농가 섭외 중", price=36200, alert="Y"),
    ]


def random_rows(rng, start=1101, count=109):
    rows = []
    for i in range(count):
        code, name, transport = rng.choice(PRODUCTS)
        partner = rng.choice(list(PARTNERS))
        status = rng.choices(["준비중", "출고", "배송중", "완료", "지연", "변경"], [20, 20, 25, 25, 5, 5])[0]
        scheduled = "2026-11-21" if status == "완료" else f"2026-11-{rng.choice([21, 22, 23])}"
        updated = NOW - timedelta(hours=rng.randint(1, 20), minutes=rng.randint(0, 59))
        reason = rng.choice(PUBLIC_REASONS) if status in ("지연", "변경") else ""
        alert = "Y" if transport == "냉장" and rng.random() < 0.08 else "N"
        rows.append({
            "order_no": f"ORD-{start + i}", "partner_code": partner, "partner_name": PARTNERS[partner],
            "product_code": code, "product_name": name, "qty": rng.randint(1, 12), "transport": transport,
            "scheduled_date": scheduled, "status": status, "public_reason": reason,
            "updated_at": fmt(updated), "internal_memo": rng.choice(RANDOM_MEMOS),
            "supply_price": rng.randrange(8000, 90000, 100), "temp_alert": alert,
        })
    return rows


def main():
    rng = random.Random(2026)
    rows = special_rows() + random_rows(rng)
    data_dir = ROOT / "data"
    data_dir.mkdir(exist_ok=True)
    # utf-8-sig: Excel에서 한글이 깨지지 않도록
    with open(data_dir / "orders.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    (data_dir / "handoffs.json").write_text("[]\n", encoding="utf-8")
    print(f"orders.csv: {len(rows)}행 생성 (기준 시각 {fmt(NOW)})")


if __name__ == "__main__":
    main()
