""" DB 연결을 생성하고 DB에 데이터를 적재합니다"""
import concurrent.futures
import time
from datetime import datetime

def load_init(detail_list):
    """
    앱 상세 정보 데이터를 처리하여 load_to_db에 넣을 수 있게 반환

    Parameters
    ----------
    detail_list : list
        DESCRIPTION.

    Returns
    -------
    app : TYPE
        DESCRIPTION.
    description : TYPE
        DESCRIPTION.
    app_genre : TYPE
        DESCRIPTION.
    app_pub : TYPE
        DESCRIPTION.
    app_dev : TYPE
        DESCRIPTION.
    recommendation : TYPE
        DESCRIPTION.
    publisher : TYPE
        DESCRIPTION.
    developer : TYPE
        DESCRIPTION.
    genre : TYPE
        DESCRIPTION.

    """
    app, description, app_genre, app_pub, app_dev, recommendation = [], [], [], [], [], []
    publisher, developer = {}, {}
    genre = {}
    app_ids = set()
    
    start = time.time()
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=200)
    
    # 저장 부분
    pub_id, dev_id = 1, 1
    def load_detail(app_detail):
        nonlocal pub_id, dev_id
        if not app_detail: 
            return
        if not app_detail["price_overview"]: 
            return
        if app_detail["basegame_id"]:
            if app_detail["basegame_id"] not in app_ids:
                return
        if "date" in app_detail["release_date"]:
            try:
                date = datetime.strptime(app_detail["release_date"]["date"], "%Y년 %m월 %d일")
            except:
                date = None
        app_ids.add(app_detail["app_id"])
        app.append((app_detail["app_id"], app_detail["name"], app_detail["header_url"],
                    date, app_detail["contents_type"], app_detail["basegame_id"]))
        description.append((app_detail["app_id"], app_detail["short_description"],
                   app_detail["min_requirement"], app_detail["rec_requirement"]))
        recommendation.append((app_detail["app_id"], app_detail["recommendation"]))
        for gen in app_detail["genres"]:
            genre[int(gen["id"])] = gen["description"]
            app_genre.append((app_detail["app_id"], int(gen["id"])))
        
        if  app_detail["publishers"]:
            for pub_name in app_detail["publishers"]:
                if pub_name not in publisher:
                    publisher[pub_name] = pub_id
                    pub_id += 1
                app_pub.append((app_detail["app_id"], publisher[pub_name]))
                
        if  app_detail["developers"]:
            for dev_name in app_detail["developers"]:
                if dev_name not in developer:
                    developer[dev_name] = dev_id
                    dev_id += 1
                app_dev.append((app_detail["app_id"], developer[dev_name]))

    threads = []
    for detail in detail_list:
        threads.append(pool.submit(load_detail, detail))

    concurrent.futures.wait(threads)
    print(time.time() - start)
    
    return app, description, app_genre, app_pub, app_dev, recommendation, publisher, developer, genre

def load_to_db(cursor, app, description, app_genre, app_pub, app_dev, recommendation, publisher, developer, genre):
    """
    load_init의 데이터를 받아서 db에 적재함

    Parameters
    ----------
    cursor : psycopg.Cursor
        psycopg의 cursor
    app : list
        DESCRIPTION.
    description : list
        DESCRIPTION.
    app_genre : list
        DESCRIPTION.
    app_pub : list
        DESCRIPTION.
    app_dev : list
        DESCRIPTION.
    recommendation : list
        DESCRIPTION.
    publisher : dict
        DESCRIPTION.
    developer : dict
        DESCRIPTION.
    genre : dict
        DESCRIPTION.

    Returns
    -------
    None.

    """
    start = time.time()
    # App
    query = "COPY app (app_id, name, header_url, release_date, type, basegame_id) FROM STDIN"
    with cursor.copy(query) as copy:
        for detail in app:
            copy.write_row(detail)
    print("Done App")
    # Description
    query = "COPY description (app_id, short_description, min_requirement, rec_requirement) FROM STDIN"
    with cursor.copy(query) as copy:
        for data in description:
            copy.write_row(data)
    print("Done des")
    # Genre
    query = "COPY genre (genre_id, genre) FROM STDIN"
    with cursor.copy(query) as copy:
        for data in genre.items():
            copy.write_row(data)
    print("Done genre")
    # App_Genre
    cursor.execute("CREATE TEMPORARY TABLE tmp_app_genre (app_id int, genre_id int) ON COMMIT DROP")
    query = "COPY tmp_app_genre (app_id, genre_id) FROM STDIN"
    with cursor.copy(query) as copy:
        for data in app_genre:
            copy.write_row(data)
    cursor.execute("INSERT INTO app_genre(app_id, genre_id) SELECT app_id, genre_id FROM tmp_app_genre ON CONFLICT DO NOTHING")
    print("Done app_genre")
    # Recommendation
    query = "COPY recommendation (app_id, count) FROM STDIN"
    with cursor.copy(query) as copy:
        for data in recommendation:
            copy.write_row(data)
    print("Done rec")
    # Developer
    query = "COPY developer (name, developer_id) FROM STDIN"
    with cursor.copy(query) as copy:
        for data in developer.items():
            copy.write_row(data)
    print("Done dev")
    # Publisher
    query = "COPY publisher (name, publisher_id) FROM STDIN"
    with cursor.copy(query) as copy:
        for data in publisher.items():
            copy.write_row(data)
    print("Done pub")
    # App_Dev
    cursor.execute("CREATE TEMPORARY TABLE tmp_app_dev (app_id int, developer_id int) ON COMMIT DROP")
    query = "COPY tmp_app_dev (app_id, developer_id) FROM STDIN"
    with cursor.copy(query) as copy:
        for data in app_dev:
            copy.write_row(data)
    cursor.execute("INSERT INTO app_dev (app_id, developer_id) SELECT app_id, developer_id FROM tmp_app_dev ON CONFLICT DO NOTHING")
    print("Done app_dev")
    # App_Pub
    cursor.execute("CREATE TEMPORARY TABLE tmp_app_pub (app_id int, publisher_id int) ON COMMIT DROP")
    query = "COPY tmp_app_pub (app_id, publisher_id) FROM STDIN"
    with cursor.copy(query) as copy:
        for data in app_pub:
            copy.write_row(data)
    cursor.execute("INSERT INTO app_pub (app_id, publisher_id) SELECT app_id, publisher_id FROM tmp_app_pub ON CONFLICT DO NOTHING")
    print("Done app_pub")
    print(time.time() - start)

def update_price(cursor, detail_list):
    """

    Parameters
    ----------
    cursor : TYPE
        DESCRIPTION.
    detail_list : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    result = []
    today = datetime.now().strftime("%Y-%m-%d")
    
    def get_price(app_detail):
        if not app_detail: 
            return
        if not app_detail["price_overview"]: 
            return

        result.append((today, 1, app_detail["app_id"],
         app_detail["price_overview"]["final"] // 100, app_detail["price_overview"]["initial"] // 100,
         app_detail["price_overview"]["discount_percent"]))
    
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=200)
    threads = []
    for detail in detail_list:
        threads.append(pool.submit(get_price, detail))
    concurrent.futures.wait(threads)
    print(len(result))
    
    cursor.execute("CREATE TEMPORARY TABLE tmp_price (date date, store_id int, app_id int, price int, init_price int, discount int) ON COMMIT DROP")
    query = "COPY tmp_price (date, store_id, app_id, price, init_price, discount) FROM STDIN"
    with cursor.copy(query) as copy:
        for price in result:
            copy.write_row(price)
    cursor.execute("INSERT INTO price (date, store_id, app_id, price, init_price, discount) SELECT date, store_id, app_id, price, init_price, discount FROM tmp_price ON CONFLICT DO NOTHING")
    print("Done Price")
