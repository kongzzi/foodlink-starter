import pytest

import logic


@pytest.fixture(autouse=True)
def fixed_now_and_tmp_handoffs(monkeypatch, tmp_path):
    monkeypatch.setenv("FOODLINK_NOW", "2026-11-21T09:00:00")
    monkeypatch.setattr(logic, "HANDOFFS_PATH", tmp_path / "handoffs.json")


def test_load_orders():
    orders = logic.load_orders()
    assert len(orders) == 120
    assert orders[0]["order_no"] == "ORD-1001"

# TODO (5차시) /tests로 도구별 테스트를 생성한다. 반드시 포함할 것:
#   - 존재하지 않는 주문번호
#   - 24시간 넘게 갱신되지 않은 주문 (ORD-1010)
#   - 비공개 필드(internal_memo, supply_price, temp_alert)가 응답에 없음
