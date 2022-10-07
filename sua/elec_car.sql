use elec_car;

# 충전소별_충전구분(speed) 테이블 생성
create table 충전소별_충전구분
select 충전구분, 충전소명 from 구분_명_주소;


# 충전소(charge_address) 테이블 생성
create table 충전소
select distinct 충전소명, 주소 from 구분_명_주소; 


# 차량등록(car_register) 테이블 생성
create table 차량등록
select 사용본거지시읍면동_행정동기준, 연료 from 행정동별_전기차_현황; 


# 차량등록(car_register) 테이블의 인덱스 컬럼 추가
alter table 차량등록 add column ind int(11) auto_increment primary key first;
