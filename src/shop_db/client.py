"""Supabase 클라이언트 생성 모듈.

.env 의 SUPABASE_URL, SUPABASE_KEY 를 읽어 클라이언트를 하나 만들어 재사용합니다.
"""

import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

_client: Client | None = None


def get_client() -> Client:
    """Supabase 클라이언트를 반환합니다. (처음 호출 때만 생성)"""
    global _client
    if _client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise RuntimeError(
                ".env 에 SUPABASE_URL, SUPABASE_KEY 가 없습니다. "
                ".env.example 을 .env 로 복사해서 값을 채워주세요."
            )
        _client = create_client(url, key)
    return _client
