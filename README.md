# 쇼핑몰 DB - Supabase 연동 과제

PostgreSQL(Supabase)로 **회원 / 상품 / 주문** 테이블을 만들고,
Python(uv) + Supabase SDK로 CRUD를 구현한 과제입니다.

## 기술 스택
- Python 3.13, uv
- Supabase (PostgreSQL), supabase-py
- python-dotenv

## 프로젝트 구조
```
.
├── sql/
│   ├── 01_schema.sql        # 테이블 생성 (CREATE / ALTER / DROP)
│   ├── 02_dml_verify.sql    # INSERT / UPDATE / DELETE + 제약조건 검증
│   └── 03_transaction.sql   # COMMIT / ROLLBACK
├── src/shop_db/
│   ├── __init__.py          # 실행 진입점 (main)
│   ├── client.py            # Supabase 클라이언트
│   ├── members.py           # 회원 CRUD
│   ├── products.py          # 상품 CRUD
│   └── orders.py            # 주문 CRUD
├── docs/images/             # README 캡처 이미지
├── .env.example             # 환경 변수 예시 (복사해서 .env 로 사용)
└── pyproject.toml
```

## 실행 방법
```bash
uv sync
cp .env.example .env   # SUPABASE_URL, SUPABASE_KEY 입력
uv run shop-db
```

## 테이블 명세

### members (회원)
| 컬럼 | 타입 | 제약조건 |
| --- | --- | --- |
| id | BIGINT | **PK**, IDENTITY |
| email | VARCHAR(255) | NOT NULL, UNIQUE |
| name | VARCHAR(50) | NOT NULL |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() |

### products (상품)
| 컬럼 | 타입 | 제약조건 |
| --- | --- | --- |
| id | BIGINT | **PK**, IDENTITY |
| name | VARCHAR(100) | NOT NULL |
| price | INTEGER | NOT NULL, CHECK (price >= 0) |
| stock | INTEGER | NOT NULL, DEFAULT 0, CHECK (stock >= 0) |

### orders (주문)
| 컬럼 | 타입 | 제약조건 |
| --- | --- | --- |
| id | BIGINT | **PK**, IDENTITY |
| member_id | BIGINT | NOT NULL, **FK → members(id)** |
| product_id | BIGINT | NOT NULL, **FK → products(id)** |
| quantity | INTEGER | NOT NULL, CHECK (quantity > 0) |
| ordered_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() |

<!-- TODO: ERD 또는 Table Editor 캡처 (PK/FK 보이게) -->
<!-- ![schema](docs/images/schema.png) -->

## 동작 캡처

### 1. 테이블 생성
<!-- TODO -->

### 2. 데이터 변경 및 검증 (INSERT / UPDATE / DELETE)
<!-- TODO: 변경 전 / 후 SELECT 캡처 -->

### 3. 제약조건 위반 확인
<!-- TODO: CHECK / UNIQUE / FK 위반 에러 캡처 -->

### 4. 트랜잭션 (COMMIT / ROLLBACK)
<!-- TODO -->

### 5. Python CRUD 실행 결과
<!-- TODO: uv run shop-db 터미널 결과 + Supabase 테이블 화면 -->
