import psycopg2
import requests
import json

dbname = ""
user = ""
password = ""
host = ""
port = 0

conn = psycopg2.connect(dbname = dbname, user= user,
                        password= password, host= host, port= port)
cur = conn.cursor()
app_list_get = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
app_json = json.loads(app_list_get.text)

for app in app_json["applist"]["apps"]:
    if app["name"]:
        try:
            cur.execute("INSERT INTO app (appid, name) VALUES (%s, %s)", (app["appid"], app["name"]))
        except Exception as e:
            print(e)
            print(app["appid"], app["name"])
cur.execute("commit;")
cur.close()