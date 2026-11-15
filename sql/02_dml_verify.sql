-- =========================================================
-- 02_dml_verify.sql : 데이터 변경 (DML) + 전후 검증
-- 각 변경 전후로 SELECT 결과를 캡처해서 README 에 넣으세요.
-- =========================================================

-- 1) INSERT : 샘플 데이터
INSERT INTO members (email, name) VALUES
    ('kim@test.com', '김철수'),
    ('ko@test.com', '고영희');

INSERT INTO products (name, price, stock) VALUES
    ('고양이 모자', 5800, 3),
    ('강아지 신발', 9900, 3);

INSERT INTO orders (member_id, product_id, quantity) VALUES
    (1, 2, 1),
    (2, 1, 2);

-- 2) UPDATE : 변경 전 SELECT -> UPDATE -> 변경 후 SELECT
SELECT * FROM products WHERE id = 1;          -- 변경 전 📸
UPDATE products SET price = 15000 WHERE id = 1;
SELECT * FROM products WHERE id = 1;          -- 변경 후 📸

-- 3) DELETE : 삭제 전 SELECT -> DELETE -> 삭제 후 SELECT
INSERT INTO members (email, name) VALUES
    ('lee@test.com', '이영수');

SELECT * FROM members;
DELETE FROM members WHERE id = 3 RETURNING *;
SELECT * FROM members;

-- ---------------------------------------------------------
-- 제약조건 위반 확인 (에러가 나는 게 정상! 에러 화면 캡처)
-- ---------------------------------------------------------
-- CHECK 위반 : 음수 가격 상품 INSERT -> products_price_check
INSERT INTO products (name, price, stock) VALUES
    ('고양이 목걸이', -5800, 2);

-- UNIQUE 위반 : 이미 있는 email 로 UPDATE -> members_email_key
SELECT * FROM members;
UPDATE members SET email = 'kim@test.com' WHERE id = 2;

-- FK 위반 : 주문이 있는 회원 DELETE -> orders_member_id_fkey
SELECT * FROM members;
DELETE FROM members WHERE id = 1 RETURNING *;
