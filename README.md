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
| status | VARCHAR(20) | NOT NULL, DEFAULT 'ORDERED' (ALTER로 추가) |

#### PK / FK 확인 (information_schema 조회)
![PK FK 확인](docs/images/schema_create_table_1.png)

## 동작 캡처

### 1. 테이블 생성 (`sql/01_schema.sql`)

#### CREATE TABLE
| members | products | orders |
| --- | --- | --- |
| ![members](docs/images/schema_create_members.png) | ![products](docs/images/schema_create_products.png) | ![orders](docs/images/schema_create_orders.png) |

#### ALTER / DROP
![ALTER DROP](docs/images/schema_alter_drop.png)

#### 생성된 테이블
![테이블 목록](docs/images/schema_create_table_2.png)

### 2. 데이터 변경 및 검증 (`sql/02_dml_verify.sql`)

#### INSERT
| 테이블 | 실행 | 결과 |
| --- | --- | --- |
| members | ![](docs/images/dml_insert_members.png) | ![](docs/images/dml_insert_members_view.png) |
| products | ![](docs/images/dml_insert_products.png) | ![](docs/images/dml_insert_products_view.png) |
| orders | ![](docs/images/dml_insert_orders.png) | ![](docs/images/dml_insert_orders_view.png) |

주문 조회 (회원·상품 JOIN)

![주문 조회](docs/images/dml_select_orders_view.png)

#### UPDATE - 상품 가격 변경 (5800 → 15000)
| 변경 전 | UPDATE 실행 | 변경 후 |
| --- | --- | --- |
| ![](docs/images/dml_update_products_price_1.png) | ![](docs/images/dml_update_products_price_2.png) | ![](docs/images/dml_update_products_price_3.png) |

#### DELETE - 주문 없는 회원 삭제
| 삭제 전 | DELETE 실행 | 삭제 후 |
| --- | --- | --- |
| ![](docs/images/dml_delete_members_1.png) | ![](docs/images/dml_delete_members_2.png) | ![](docs/images/dml_delete_members_3.png) |

### 3. 제약조건 위반 확인
| 제약조건 | 시도 | 결과 |
| --- | --- | --- |
| CHECK | 음수 가격 상품 INSERT | `products_price_check` 위반으로 거부 |
| UNIQUE | 다른 회원의 email을 이미 있는 값으로 UPDATE | `members_email_key` 위반으로 거부 |
| FOREIGN KEY | 주문이 있는 회원 DELETE | `orders_member_id_fkey` 위반으로 거부 |

#### CHECK
![CHECK 위반](docs/images/dml_check.png)

#### UNIQUE
![UNIQUE 위반](docs/images/dml_unique.png)

#### FOREIGN KEY
![FK 위반](docs/images/dml_fk.png)

### 4. 트랜잭션 (`sql/03_transaction.sql`)
주문 생성(`orders` INSERT)과 재고 차감(`products` UPDATE)을 하나의 트랜잭션으로 묶어,
둘 다 반영되거나 둘 다 반영되지 않도록 처리합니다.

#### 성공 시나리오 → COMMIT
고양이 모자(id 1) 1개 주문: 주문 1건 추가 + 재고 3 → 2

| 실행 전 (재고 3) | 트랜잭션 실행 | 실행 후 (재고 2) |
| --- | --- | --- |
| ![](docs/images/transaction_commit_1.png) | ![](docs/images/transaction_commit_2.png) | ![](docs/images/transaction_commit_3.png) |

#### 실패 시나리오 → ROLLBACK
재고 2개인 상품을 10개 주문 → 재고가 -8이 되어 `products_stock_check` 위반 → 트랜잭션 전체 취소

| 트랜잭션 실행 (CHECK 위반 에러) | 실행 후 재고 (2 그대로) | 실행 후 주문 (10개 주문 없음, 3건 유지) |
| --- | --- | --- |
| ![](docs/images/transaction_rollback_1.png) | ![](docs/images/transaction_rollback_2.png) | ![](docs/images/transaction_rollback_3.jpg) |

에러 앞에서 실행된 주문 INSERT까지 함께 취소되어, **주문만 들어가고 재고는 그대로인 부분 반영이 발생하지 않음**을 확인했습니다.

### 5. Python CRUD 실행 결과
<!-- TODO: uv run shop-db 터미널 결과 + Supabase 테이블 화면 -->
