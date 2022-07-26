import requests
import json

def get_applist():
    """
    steam api를 호출하여 applist를 받아 제네레이터를 생성하는 함수
    
    Yields
    ------
    app["appid"]: int
        스팀 어플리케이션 고유의 id
    
    app["name"] : str
        스팀 어플리케이션의 제목

    """

    app_list_get = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
    app_json = json.loads(app_list_get.text)
    
    for app in app_json["applist"]["apps"]:
        yield app["appid"], app["name"]