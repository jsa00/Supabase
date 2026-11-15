-- =========================================================
-- 03_transaction.sql : 트랜잭션 (TCL)
-- 시나리오: 주문 생성 + 재고 차감을 하나의 트랜잭션으로 묶기
-- =========================================================

-- [성공 시나리오] -> COMMIT
-- 실행 전 재고 확인
SELECT * FROM products WHERE id = 1;

BEGIN;
INSERT INTO orders (member_id, product_id, quantity) VALUES (1, 1, 1);
UPDATE products SET stock = stock - 1 WHERE id = 1;
COMMIT;

-- 실행 후 주문 추가 + 재고 차감이 둘 다 반영됐는지 확인
SELECT * FROM orders;
SELECT * FROM products WHERE id = 1;

-- [실패 시나리오] -> ROLLBACK
-- 재고보다 많이 주문 -> CHECK (stock >= 0) 위반 -> 에러
BEGIN;
INSERT INTO orders (member_id, product_id, quantity) VALUES (2, 1, 10);
UPDATE products SET stock = stock - 10 WHERE id = 1;   -- stock -8 → CHECK 위반
ROLLBACK;
-- 에러로 트랜잭션 전체가 취소됨 -> 주문이 남지 않고 재고도 그대로인지 확인
SELECT * FROM orders;
SELECT * FROM products WHERE id = 1;