""" DB 연결을 생성하고 DB에 데이터를 적재합니다"""
import concurrent.futures
import time
from datetime import datetime

def load_init(detail_list):
    app, description, app_genre, app_pub, app_dev, recommendation = [], [], [], [], [], []
    publisher, developer = {}, {}
    genre = {}
    
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
        if app_detail["release_date"]["coming_soon"]: 
            return
        if app_detail["contents_type"] != "game":
            return
        if "date" in app_detail["release_date"]:
            try:
                date = datetime.strptime(app_detail["release_date"]["date"], "%Y년 %m월 %d일")
            except:
                date = None
        
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
    query = "COPY app_genre (app_id, genre_id) FROM STDIN"
    with cursor.copy(query) as copy:
        for data in app_genre:
            copy.write_row(data)
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
    query = "COPY app_dev (app_id, developer_id) FROM STDIN"
    with cursor.copy(query) as copy:
        for data in app_dev:
            copy.write_row(data)
    print("Done app_dev")
    # App_Pub
    query = "COPY app_pub (app_id, publisher_id) FROM STDIN"
    with cursor.copy(query) as copy:
        for data in app_pub:
            copy.write_row(data)
    print("Done app_pub")
    cursor.execute("commit")
    print(time.time() - start)
    