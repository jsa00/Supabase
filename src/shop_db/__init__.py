"""쇼핑몰 DB 과제 실행 진입점.

실행: uv run shop-db
    pyproject.toml 의 [project.scripts] shop-db = "shop_db:main" 설정에 따라
    이 파일의 main() 이 실행된다.
"""

import time

from shop_db.client import get_client


def check_connection() -> None:
    """Supabase 연결 확인: 세 테이블을 1건씩 조회한다."""
    client = get_client()
    for table in ("members", "products", "orders"):
        # limit(1): 연결 확인용이라 한 행만 가져온다.
        res = client.table(table).select("*").limit(1).execute()
        print(f"[{table}] 연결 OK, 조회 결과: {res.data}")


def section(title: str) -> None:
    """실행 결과를 단계별로 구분해서 보기 쉽게 출력한다."""
    print(f"\n========== {title} ==========")


def demo_crud() -> None:
    """회원 / 상품 / 주문 CRUD 시연: 생성 -> 조회 -> 수정 -> 삭제.

    기존 데이터와 충돌하지 않도록 시연용 데이터를 새로 만들고, 마지막에 모두 삭제한다.
    """
    from shop_db import members, orders, products

    # email 은 UNIQUE 라서 같은 값으로 두 번 실행하면 에러가 난다.
    # 현재 시각(초)을 붙여 실행할 때마다 다른 email 을 사용한다.
    email = f"crud_{int(time.time())}@test.com"

    # ---------- Create ----------
    section("1. Create")
    # 생성 함수는 DB 가 만든 id 가 담긴 행(dict)을 돌려준다.
    # 이 id 를 변수에 받아 두고 이후 조회/수정/삭제에 사용한다. (id 를 숫자로 고정하지 않음)
    member = members.create_member(email, "이영수")
    print("회원 생성:", member)
    product = products.create_product("토끼 머리띠", 7000, 5)
    print("상품 생성:", product)
    # 주문은 회원/상품을 FK 로 참조하므로, 회원과 상품을 먼저 만든 뒤에 생성한다.
    order = orders.create_order(member["id"], product["id"], 2)
    print("주문 생성:", order)

    # ---------- Read ----------
    section("2. Read")
    print("회원 단건 조회:", members.get_member(member["id"]))
    print("상품 단건 조회:", products.get_product(product["id"]))
    print("회원별 주문 조회:", orders.get_orders_by_member(member["id"]))
    print("전체 회원 수:", len(members.get_members()))
    print("전체 상품 수:", len(products.get_products()))
    print("전체 주문 수:", len(orders.get_orders()))

    # ---------- Update ----------
    section("3. Update")
    print("회원 이름 수정:", members.update_member(member["id"], "김춘식"))
    print("상품 가격/재고 수정:", products.update_product(product["id"], price=6500, stock=10))
    print("주문 수량 수정:", orders.update_order_quantity(order["id"], 3))

    # ---------- Delete ----------
    section("4. Delete")
    # FK 때문에 삭제 순서가 중요하다.
    # 주문(자식)이 회원/상품(부모)을 참조하고 있으므로 주문을 먼저 지워야
    # 회원과 상품을 지울 수 있다.
    orders.delete_order(order["id"])
    print("주문 삭제 후 조회:", orders.get_orders_by_member(member["id"]))  # [] 이면 삭제됨
    members.delete_member(member["id"])
    print("회원 삭제 후 조회:", members.get_member(member["id"]))  # None 이면 삭제됨
    products.delete_product(product["id"])
    print("상품 삭제 후 조회:", products.get_product(product["id"]))  # None 이면 삭제됨


def main() -> None:
    check_connection()
    demo_crud()
