"""회원(members) 테이블 CRUD.

사용 예시 (supabase-py):
    get_client().table("members").insert({...}).execute()
    get_client().table("members").select("*").execute()
    get_client().table("members").update({...}).eq("id", member_id).execute()
    get_client().table("members").delete().eq("id", member_id).execute()
결과 데이터는 response.data (list[dict]) 에 들어 있습니다.
"""

from shop_db.client import get_client

TABLE = "members"


def create_member(email: str, name: str) -> dict:
    """회원을 추가하고, 추가된 행을 반환합니다."""
    # TODO: insert 구현
    raise NotImplementedError


def get_members() -> list[dict]:
    """전체 회원 목록을 반환합니다."""
    # TODO: select 구현
    raise NotImplementedError


def get_member(member_id: int) -> dict | None:
    """id 로 회원 한 명을 조회합니다. 없으면 None."""
    # TODO: select + eq 구현
    raise NotImplementedError


def update_member(member_id: int, name: str) -> dict:
    """회원 이름을 수정하고, 수정된 행을 반환합니다."""
    # TODO: update + eq 구현
    raise NotImplementedError


def delete_member(member_id: int) -> None:
    """회원을 삭제합니다. (주문이 있으면 FK 제약으로 실패하는지 확인해보세요)"""
    # TODO: delete + eq 구현
    raise NotImplementedError
