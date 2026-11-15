"""주문(orders) 테이블 CRUD. 요청 흐름 설명은 members.py 상단 주석 참고."""

from shop_db.client import get_client

TABLE = "orders"

# 주문을 조회할 때 FK 로 연결된 회원/상품 정보도 함께 가져오는 select 문자열이다.
#   "*"                       : orders 테이블의 모든 컬럼
#   "members(name)"           : member_id 로 연결된 회원의 name
#   "products(name, price)"   : product_id 로 연결된 상품의 name, price
# SQL 의 JOIN 과 같은 역할이며, 결과에는 {"members": {...}, "products": {...}} 형태로 붙는다.
WITH_RELATIONS = "*, members(name), products(name, price)"

client = get_client()


# ==================== Create ====================
def create_order(member_id: int, product_id: int, quantity: int) -> dict:
    """주문을 추가하고, 추가된 행을 반환한다."""
    # INSERT INTO orders (member_id, product_id, quantity) VALUES (...)
    # - 존재하지 않는 member_id / product_id 면 FK 위반으로 APIError
    # - quantity <= 0 이면 CHECK 위반으로 APIError
    # - ordered_at, status 는 DB 기본값(now(), 'ORDERED')으로 채워진다.
    # 참고: 재고 차감은 하지 않는다. 주문 + 재고 차감을 함께 처리하는 것은
    #       sql/03_transaction.sql 의 트랜잭션에서 다룬다.
    res = (
        client.table(TABLE)
        .insert({"member_id": member_id, "product_id": product_id, "quantity": quantity})
        .execute()
    )
    return res.data[0]


# ==================== Read ====================
def get_orders() -> list[dict]:
    """전체 주문 목록을 반환한다. (회원 이름, 상품 이름/가격 포함)"""
    # SELECT o.*, m.name, p.name, p.price
    # FROM orders o JOIN members m ... JOIN products p ... ORDER BY o.id
    res = client.table(TABLE).select(WITH_RELATIONS).order("id").execute()
    return res.data


def get_orders_by_member(member_id: int) -> list[dict]:
    """특정 회원의 주문 목록을 반환한다. (회원 이름, 상품 이름/가격 포함)"""
    # 위 조회에 WHERE member_id = ... 조건을 추가한 것과 같다.
    # 메서드를 줄 단위로 나눠 쓰려면 전체를 괄호 ( ) 로 감싸면 된다.
    res = (
        client.table(TABLE)
        .select(WITH_RELATIONS)
        .eq("member_id", member_id)
        .order("id")
        .execute()
    )
    return res.data


# ==================== Update ====================
def update_order_quantity(order_id: int, quantity: int) -> dict:
    """주문 수량을 수정한다."""
    # UPDATE orders SET quantity = ... WHERE id = order_id
    # PK 컬럼 이름은 order_id 가 아니라 id 다.
    res = client.table(TABLE).update({"quantity": quantity}).eq("id", order_id).execute()
    return res.data[0]


# ==================== Delete ====================
def delete_order(order_id: int) -> None:
    """주문을 삭제한다."""
    # DELETE FROM orders WHERE id = order_id
    # orders 는 다른 테이블이 참조하지 않는 "자식" 테이블이라 FK 제약 없이 바로 삭제된다.
    client.table(TABLE).delete().eq("id", order_id).execute()
