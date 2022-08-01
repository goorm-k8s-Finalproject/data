# example of using p2p
import p2p
import psycopg
import pickle

dbname = ''
user = ''
password = ''
host = ''
port = 0

with psycopg.connect(dbname = dbname, user = user,
                        password = password, host = host, port = port) as conn:
    try:
        with conn.cursor() as cur:
            with open("p2p/detail_list.pickle","rb") as fr:
                detail_list = pickle.load(fr)
        
            data = p2p.load_init(detail_list)
        
            p2p.load_to_db(cur, *data)
    except BaseException:
        conn.rollback()
    else:
        conn.commit()
    finally:
        conn.close()
