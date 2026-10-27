"""배송 안내 도구의 핵심 로직 (MCP와 무관한 순수 함수).

server.py는 이 함수들을 MCP 도구로 노출하기만 한다.
로직을 분리해 두면 MCP 없이도 pytest로 검증할 수 있다.

TODO 표시된 함수를 차시별로 Copilot과 함께 구현한다.
"""
import csv
import json
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(os.environ.get("FOODLINK_DATA_DIR", Path(__file__).resolve().parent / "data"))
HANDOFFS_PATH = Path(os.environ.get("FOODLINK_HANDOFFS", DATA_DIR / "handoffs.json"))
FRESH_HOURS = 24

# 고객에게 보여도 되는 필드. internal_memo, supply_price, temp_alert 는 절대 포함하지 않는다.
PUBLIC_FIELDS = [
    "order_no", "partner_name", "product_code", "product_name", "qty",
    "transport", "scheduled_date", "status", "public_reason", "updated_at",
]
HANDOFF_REASONS = ("주문 없음", "데이터 오래됨", "지연·변경 문의", "기타")
HANDOFF_STATUSES = ("접수", "처리중", "완료")


def now():
    """시뮬레이션 현재시각. FOODLINK_NOW 환경변수가 있으면 그 값을 쓴다."""
    value = os.environ.get("FOODLINK_NOW")
    return datetime.fromisoformat(value) if value else datetime.now()


def load_orders():
    with open(DATA_DIR / "orders.csv", newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["qty"] = int(row["qty"])
    return rows


# TODO (3차시) 주문 하나에서 PUBLIC_FIELDS에 있는 항목만 골라 새 딕셔너리로 반환한다.
#   고객에게 보여도 되는 정보만 내보내는 유일한 통로로 쓴다.
def public_view(order):
    raise NotImplementedError


# TODO (4차시) 마지막 갱신 후 FRESH_HOURS(24시간)가 지났는지 판정한다.
#   반환: {"as_of", "age_hours"(소수 첫째 자리), "is_fresh"}
def freshness(order):
    raise NotImplementedError


# TODO (3차시) 주문번호, 거래처명, 상품코드 일부, 상품명으로 주문을 검색한다.
#   반환: {"query", "total", "results", "truncated"}  (results는 최대 limit건)
def search_orders(query, limit=10):
    raise NotImplementedError


# TODO (4차시) 주문번호 하나의 현재 상태, 기준 시점(as_of), 최신성(24시간)을 반환한다.
#   데이터가 없거나 오래되었으면 needs_handoff=True 와 안내(guidance)를 포함한다.
def get_delivery_status(order_no):
    raise NotImplementedError


# TODO (4차시) 이관 요청을 data/handoffs.json에 등록한다. 같은 주문·사유의 미완료 요청은 중복 등록하지 않는다.
def create_handoff(order_no, reason, summary):
    raise NotImplementedError


# TODO (8차시) 담당자 전용 기능
def list_handoffs(status=None):
    raise NotImplementedError


def update_handoff(handoff_id, status):
    raise NotImplementedError


# TODO (9차시) 예정일 기준 일일 현황 집계
def daily_report(date):
    raise NotImplementedError
