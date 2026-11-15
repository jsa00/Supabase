"""주문(orders) 테이블 CRUD. 작성 방법은 members.py 상단 주석 참고.

팁: select("*, members(name), products(name, price)") 처럼 쓰면
FK 로 연결된 회원/상품 정보를 함께 조회할 수 있습니다.
"""

from shop_db.client import get_client

TABLE = "orders"


def create_order(member_id: int, product_id: int, quantity: int) -> dict:
    """주문을 추가하고, 추가된 행을 반환합니다."""
    # TODO
    raise NotImplementedError


def get_orders() -> list[dict]:
    """전체 주문 목록을 반환합니다."""
    # TODO
    raise NotImplementedError


def get_orders_by_member(member_id: int) -> list[dict]:
    """특정 회원의 주문 목록을 반환합니다."""
    # TODO
    raise NotImplementedError


def update_order_quantity(order_id: int, quantity: int) -> dict:
    """주문 수량을 수정합니다."""
    # TODO
    raise NotImplementedError


def delete_order(order_id: int) -> None:
    """주문을 삭제합니다."""
    # TODO
    raise NotImplementedError
