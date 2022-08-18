# 개요
p2p의 데이터 수집 및 데이터베이스 설계 레포입니다.

데이터베이스로는 PostgreSQL ver. 14.2를 사용하였고 가용성을 보장하기 위해 AWS RDS 상에서 작업하였습니다.
데이터 수집은 Python 3.8을 사용하여 [Steam web api](https://partner.steamgames.com/doc/api?l=koreana)와 통신하여 데이터를 수집하고 psycopg3 라이브러리를 활용하여 DB에 적재하였습니다. 

## ERD

![ERD](attached/erd.png)

- App: GetSteamAppList api에서 제공하는 14만 개 가량의 스팀 게임의 app_id와 name을 저장하는 릴레이션
    - **app_id**: int, pk, 스팀 게임의 app_id
    - name: varchar(65532), 게임의 이름
    - header_url: varchar(65532), 헤더 이미지의 url
    - release_date: date, 게임의 공개일자
    - type: varchar(50), 게임의 유형(game, dlc 등 자세한 도메인 파악 필요), 도메인이 파악되면 데이터타입 변경이나 별도 릴레이션 생성 등의 조치 가능성도 있음
    - basegamee_id: int, fk(App(app_id)), DLC 컨텐츠의 경우 원본 게임의 app_id를 저장
- Recommendation: 추천 수
    - **app_id:** int, pk, fk(App(app_id)) cascade, App 릴레이션에서 참조
    - count: int, 추천 수
- DLC: appdetails에서 제공하는 dlc 목록이 다중 값 속성이기 때문에 별도로 분리한 릴레이션
    - **app_id**: int, pk, fk(App(app_id)) cascade, dlc를 가지는 원본 게임의 id
    - **dlc_id**: int, pk, fk(App(app_id)) cascade, dlc의 id
- Store: 가격 정보의 구분을 위한 상점 정보
    - **store_id**: serial, pk, 인조키
    - store: varchar(50), Steam, Epic Games, Directg(steam), Directg(Epic)
- Price: 날짜의 가격 저장하는 릴레이션
    - **date**: date, pk, 날짜
    - **store_id**: serial, pk, fk(store(store_id)), 어느 곳에서 판매하는 가격인지
    - **app_id**:  int, pk, fk(App(app_id)),  게임의 아이디
    - price: int, 할인이 적용된 현재 판매가
    - init_price: int, 할인 전 원래 가격
    - discount: int, 할인율
- Developer: 개발사
    - **developer_id**: serial, pk, 개발사의 인조키
    - name: varchar(200), 개발사명
- App_Dev: appdetails에서 제공하는 개발사 목록이 다중 값 속성이기 때문에 장르 릴레이션과의 관계를 나타내는 릴레이션
    - **developer_id**: int, pk, fk(developer(developer_id))
    - **app_id**: int, pk, fk(App(app_id))
- Publisher: 공급사
    - **publisher_id**: serial, pk, 공급사의 인조키
    - name: varchar(200), 공급사명
- App_Pub: appdetails에서 제공하는 공급사 목록이 다중 값 속성이기 때문에 장르 릴레이션과의 관계를 나타내는 릴레이션
    - **publisher_id**: int, pk, fk(publisher(publisher_id))
    - **app_id**: int, pk, fk(App(app_id))
- Genre: 게임의 장르
    - **genre_id**: int, pk, 장르의 id(스팀 제공)
    - genre: varchar(50), 장르명
- App_Genre: appdetails에서 제공하는 장르 목록이 다중 값 속성이기 때문에 장르 릴레이션과의 관계를 나타내는 릴레이션
    - **app_id**: int, pk, fk(App(app_id))
    - **genre_id**: int, pk, fk(genre(genre_id))
- Description: 게임의 설명, 요구되는 PC 사양을 저장
    - **app_id**: int, pk, fk(App(app_id))
    - short_description: text, 스팀 헤더 이미지 하단에 위치한 게임 설명
    - min_requirement: text, 요구되는 최소 사양
    - rec_requirement: text, 요구되는 권장 사양


## SQL
[DDL SQL 파일](ddl.sql)

## Python
[p2p](p2p)
[p2p를 사용한 예제 코드](example.py)