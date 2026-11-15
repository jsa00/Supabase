"""상품(products) 테이블 CRUD. 작성 방법은 members.py 상단 주석 참고."""

from shop_db.client import get_client

TABLE = "products"


def create_product(name: str, price: int, stock: int = 0) -> dict:
    """상품을 추가하고, 추가된 행을 반환합니다."""
    # TODO
    raise NotImplementedError


def get_products() -> list[dict]:
    """전체 상품 목록을 반환합니다."""
    # TODO
    raise NotImplementedError


def get_product(product_id: int) -> dict | None:
    """id 로 상품 하나를 조회합니다. 없으면 None."""
    # TODO
    raise NotImplementedError


def update_product(product_id: int, price: int | None = None, stock: int | None = None) -> dict:
    """상품 가격/재고를 수정합니다. None 인 값은 바꾸지 않습니다."""
    # TODO
    raise NotImplementedError


def delete_product(product_id: int) -> None:
    """상품을 삭제합니다."""
    # TODO
    raise NotImplementedError
