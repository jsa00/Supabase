-- =========================================================
-- 02_dml_verify.sql : 데이터 변경 (DML) + 전후 검증
-- 각 변경 전후로 SELECT 결과를 캡처해서 README 에 넣으세요.
-- =========================================================

-- 1) INSERT : 샘플 데이터
-- TODO: members 2~3건, products 2~3건, orders 2~3건 INSERT

-- 2) UPDATE : 변경 전 SELECT -> UPDATE -> 변경 후 SELECT
-- TODO

-- 3) DELETE : 삭제 전 SELECT -> DELETE -> 삭제 후 SELECT
-- TODO

-- ---------------------------------------------------------
-- 제약조건 위반 확인 (에러가 나는 게 정상! 에러 화면 캡처)
-- ---------------------------------------------------------
-- TODO: CHECK 위반   - 음수 가격 상품 INSERT
-- TODO: UNIQUE 위반  - 같은 email 회원 두 번 INSERT
-- TODO: FK 위반      - 존재하지 않는 member_id 로 주문 INSERT
-- TODO: FK 위반      - 주문이 있는 회원 DELETE
