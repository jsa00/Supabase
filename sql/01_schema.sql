-- =========================================================
-- 01_schema.sql : 테이블 생성 (DDL)
-- Supabase 대시보드 > SQL Editor 에 붙여넣고 실행하세요.
-- 관계: members 1 : N orders N : 1 products
-- =========================================================

-- 회원
CREATE TABLE members (
  id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email       VARCHAR(255) NOT NULL UNIQUE,
  name        VARCHAR(50)  NOT NULL,
  created_at  TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- 상품
CREATE TABLE products (
  id     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name   VARCHAR(100) NOT NULL,
  price  INTEGER NOT NULL CHECK (price >= 0),
  stock  INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

-- 주문
CREATE TABLE orders (
  id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  member_id   BIGINT NOT NULL REFERENCES members(id),
  product_id  BIGINT NOT NULL REFERENCES products(id),
  quantity    INTEGER NOT NULL CHECK (quantity > 0),
  ordered_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------
-- ALTER / DROP 연습 (채점 기준: CREATE·ALTER·DROP)
-- ---------------------------------------------------------
-- TODO: 주문 상태 컬럼 추가 예시
-- ALTER TABLE orders ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'ORDERED';

-- TODO: 임시 테이블을 만들었다가 DROP 해보기
-- CREATE TABLE temp_test (id INT);
-- DROP TABLE temp_test;

-- ---------------------------------------------------------
-- 스키마 확인용 쿼리 (README 캡처용: PK / FK 확인)
-- ---------------------------------------------------------
-- SELECT tc.table_name, kcu.column_name, tc.constraint_type
-- FROM information_schema.table_constraints tc
-- JOIN information_schema.key_column_usage kcu
--   ON tc.constraint_name = kcu.constraint_name
-- WHERE tc.table_name IN ('members', 'products', 'orders')
-- ORDER BY tc.table_name;
