""" DB 연결을 생성하고 DB에 데이터를 적재합니다"""

from app import get_applist
from detail import get_appdetail

def load_applist(cursor):
    """
    applist를 받아 db에 적재
    에러 발생 시 appid와 name을 출력해

    Parameters
    ----------
    cursor : psycopg.Cursor
        psycopg2 db 연결 커서

    Returns
    -------
    None.

    """
    query = "COPY app (app_id, name) FROM STDIN"
    with cursor.copy(query) as copy:
        for app in get_applist():
            if app[1]:
                copy.write_row(app)
            
    cursor.execute("commit")
    cursor.execute("select count(*) from app")
    size = cursor.fetchall()[0][0]
    print(f"{size} apps is inserted.")
 
def load_appdetail(cursor, app_id):
    details = get_appdetail(app_id)
    if not details: # 상세 정보가 없는 경우
        return
    # check app
    query = "select * from app where app_id = %s"
    cursor.execute(query, (app_id,))
    
    if not cursor.fetchall():
        query = "insert into app(app_id, name) values (%s, %s)"
        cursor.execute(query, (app_id, details["name"]))
    # check appdetail
    query = "select * from appdetail where app_id = %s"
    cursor.execute(query, (app_id,))
    if cursor.fetchall():
        cursor.execute("commit")
        return
    # insert appdetail
    query = "insert into appdetail(app_id, header_url, release_date, type)\
        values (%s, %s, to_date(%s, 'YYYY년 MM월 DD일'), %s)"
    data = (details["app_id"], details["header_url"], details["release_date"]["date"], details["contents_type"])
    cursor.execute(query, data)
    # insert dlc
    if details["dlc"]:
        for dlc_id in details["dlc"]:
            load_appdetail(cursor, dlc_id)
            cursor.execute("insert into dlc(app_id, dlc_id) values (%s, %s)", (app_id, dlc_id))
    cursor.execute("commit")
