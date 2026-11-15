"""상품(products) 테이블 CRUD. 요청 흐름 설명은 members.py 상단 주석 참고."""

from shop_db.client import get_client

TABLE = "products"
client = get_client()


# ==================== Create ====================
def create_product(name: str, price: int, stock: int = 0) -> dict:
    """상품을 추가하고, 추가된 행을 반환한다."""
    # INSERT INTO products (name, price, stock) VALUES (...)
    # price < 0 또는 stock < 0 이면 CHECK 제약 위반으로 APIError 가 발생한다.
    res = client.table(TABLE).insert({"name": name, "price": price, "stock": stock}).execute()

    # DB 가 생성한 id 가 포함된 한 행을 반환한다.
    return res.data[0]


# ==================== Read ====================
def get_products() -> list[dict]:
    """전체 상품 목록을 반환한다."""
    # SELECT * FROM products ORDER BY id
    res = client.table(TABLE).select("*").order("id").execute()
    return res.data


def get_product(product_id: int) -> dict | None:
    """id 로 상품 하나를 조회한다. 없으면 None."""
    # SELECT * FROM products WHERE id = product_id
    # PK 컬럼 이름은 product_id 가 아니라 id 다.
    res = client.table(TABLE).select("*").eq("id", product_id).execute()

    # 결과가 없으면 빈 리스트([]) -> None 반환
    return res.data[0] if res.data else None


# ==================== Update ====================
def update_product(product_id: int, price: int | None = None, stock: int | None = None) -> dict:
    """상품 가격/재고를 수정한다. None 인 값은 바꾸지 않는다."""
    # 넘겨받은 값 중 None 이 아닌 것만 골라 "바꿀 값" dict 를 만든다.
    # 예) update_product(1, price=6500)          -> {"price": 6500}
    #     update_product(1, price=6500, stock=10) -> {"price": 6500, "stock": 10}
    changes = {}
    if price is not None:
        changes["price"] = price
    if stock is not None:
        changes["stock"] = stock

    # 바꿀 값이 하나도 없으면 DB 에 요청을 보낼 필요가 없으므로 에러로 알려준다.
    if not changes:
        raise ValueError("수정할 값(price 또는 stock)을 하나 이상 넣어주세요.")

    # UPDATE products SET ... WHERE id = product_id
    res = client.table(TABLE).update(changes).eq("id", product_id).execute()
    return res.data[0]


# ==================== Delete ====================
def delete_product(product_id: int) -> None:
    """상품을 삭제한다. (주문이 있으면 FK 제약으로 실패한다)"""
    # DELETE FROM products WHERE id = product_id
    # 이 상품을 참조하는 주문(orders.product_id)이 있으면 FK 위반으로 APIError 가 발생한다.
    client.table(TABLE).delete().eq("id", product_id).execute()
