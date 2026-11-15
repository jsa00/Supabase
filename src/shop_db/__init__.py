"""쇼핑몰 DB 과제 실행 진입점.

실행: uv run shop-db
"""

from shop_db.client import get_client


def check_connection() -> None:
    """Supabase 연결 확인: 세 테이블을 1건씩 조회해봅니다."""
    client = get_client()
    for table in ("members", "products", "orders"):
        res = client.table(table).select("*").limit(1).execute()
        print(f"[{table}] 연결 OK, 조회 결과: {res.data}")


def main() -> None:
    check_connection()

    # TODO: CRUD 함수 구현 후 아래처럼 시연 코드를 작성하세요.
    # from shop_db import members, products, orders
    # print(members.create_member("test@test.com", "홍길동"))
    # print(members.get_members())
