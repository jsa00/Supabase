-- =========================================================
-- 03_transaction.sql : 트랜잭션 (TCL)
-- 시나리오: 주문 생성 + 재고 차감을 하나의 트랜잭션으로 묶기
-- =========================================================

-- [성공 시나리오] -> COMMIT
-- TODO: 실행 전 products 재고 SELECT
BEGIN;
-- TODO: orders INSERT
-- TODO: products 재고 UPDATE (stock = stock - 수량)
COMMIT;
-- TODO: 실행 후 orders / products SELECT 로 둘 다 반영됐는지 확인

-- [실패 시나리오] -> ROLLBACK
-- 재고보다 많이 주문 -> CHECK (stock >= 0) 위반 -> 에러
-- BEGIN;
-- TODO: orders INSERT
-- TODO: 재고보다 큰 수량으로 UPDATE (에러 발생)
-- ROLLBACK;
-- TODO: SELECT 로 주문이 남지 않았는지(부분 반영 X) 확인
