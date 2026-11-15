"""회원(members) 테이블 CRUD.

supabase-py 요청 흐름:
    client.table(테이블) -> 동작(insert/select/update/delete) -> 조건(eq 등) -> execute()
    - execute() 전까지는 요청을 "조립"만 하고, execute() 를 호출해야 실제로 전송된다.
    - 결과 행들은 response.data 에 list[dict] 형태로 들어 있다.
"""

from shop_db.client import get_client

# 테이블 이름을 상수로 두면, 이름이 바뀌어도 이 한 곳만 고치면 된다.
TABLE = "members"

# 모듈이 처음 import 될 때 Supabase 클라이언트를 한 번 만들어 재사용한다.
client = get_client()


# ==================== Create ====================
def create_member(email: str, name: str) -> dict:
    """회원을 추가하고, 추가된 행을 반환한다."""
    # INSERT INTO members (email, name) VALUES (...)
    # id, created_at 은 DB 기본값(IDENTITY, now())으로 자동 생성된다.
    # email 이 이미 있으면 UNIQUE 제약 위반으로 APIError 가 발생한다.
    res = client.table(TABLE).insert({"email": email, "name": name}).execute()

    # insert 결과도 리스트로 오므로, 방금 추가한 한 행만 꺼내서 반환한다.
    # (DB 가 생성한 id 를 여기서 받아 이후 조회/수정/삭제에 사용한다.)
    return res.data[0]


# ==================== Read ====================
def get_members() -> list[dict]:
    """전체 회원 목록을 반환한다."""
    # SELECT * FROM members ORDER BY id
    # order("id") 가 없으면 행 순서가 보장되지 않아 실행할 때마다 순서가 달라질 수 있다.
    res = client.table(TABLE).select("*").order("id").execute()
    return res.data


def get_member(member_id: int) -> dict | None:
    """id 로 회원 한 명을 조회한다. 없으면 None."""
    # SELECT * FROM members WHERE id = member_id
    # eq(컬럼, 값) 이 SQL 의 WHERE 컬럼 = 값 에 해당한다.
    res = client.table(TABLE).select("*").eq("id", member_id).execute()

    # 조회 결과가 없으면 빈 리스트([])가 오므로, 그때는 None 을 반환한다.
    return res.data[0] if res.data else None


# ==================== Update ====================
def update_member(member_id: int, name: str) -> dict:
    """회원 이름을 수정하고, 수정된 행을 반환한다."""
    # UPDATE members SET name = ... WHERE id = member_id
    # update() 에는 "바꿀 값", eq() 에는 "바꿀 대상을 찾는 조건"이 들어간다.
    # eq() 를 빠뜨리면 모든 행이 대상이 되므로 반드시 조건을 붙인다.
    res = client.table(TABLE).update({"name": name}).eq("id", member_id).execute()

    # 수정된 행이 리스트로 돌아오므로 첫 번째 행을 반환한다.
    return res.data[0]


# ==================== Delete ====================
def delete_member(member_id: int) -> None:
    """회원을 삭제한다. (주문이 있으면 FK 제약으로 실패한다)"""
    # DELETE FROM members WHERE id = member_id
    # 이 회원을 참조하는 주문(orders.member_id)이 있으면
    # FK 제약(orders_member_id_fkey) 위반으로 APIError 가 발생한다.
    # -> 회원을 지우려면 그 회원의 주문을 먼저 삭제해야 한다.
    client.table(TABLE).delete().eq("id", member_id).execute()
