"""
steam api를 호출하여 app의 상세 정보를 불러오는 모듈
"""
import requests
import json
import time

def get_appdetail(app_id):
    """
    steam api에서 어플리케이션 상세정보를 받아 딕셔너리 형태로 반환

    Parameters
    ----------
    app_id : int
        상세 정보를 조회할 어플리케이션 아이디

    Returns
    -------
    result : dict
        상세 정보를 담은 딕셔너리

    """

    appdetail_get = requests.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=kr&l=koreana")
    detail_json = json.loads(appdetail_get.text)
    if not detail_json:
        return
    if detail_json[f"{app_id}"]["success"] == False:
        print(appdetail_get.text)
        return
    data_json = detail_json[f"{app_id}"]["data"]
    
    result = {
        "app_id": app_id,
        "name": data_json["name"] if "name" in data_json else None,
        "header_url": data_json["header_image"] if "header_image" in data_json else None,
        "release_date": data_json["release_date"] if "release_date" in data_json else None,
        "contents_type": data_json["type"] if "type" in data_json else None,
        "recommendation": data_json["recommendations"]["total"] if "recommendations" in data_json else None,
        "dlc": data_json["dlc"] if "dlc" in data_json else None,
        "developers": data_json["developers"] if "developers" in data_json else None,
        "publishers": data_json["publishers"] if "publishers" in data_json else None,
        "genres": data_json["genres"] if "genres" in data_json else None,
        "short_description": data_json["short_description"] if "short_description" in data_json else None,
        "min_requirement": data_json["pc_requirements"]["minimum"] if "pc_requirements" in data_json and "minimum" in data_json["pc_requirements"] else None,
        "rec_requirement": data_json["pc_requirements"]["recommended"] if "pc_requirements" in data_json and "recommended" in data_json["pc_requirements"] else None,
        "is_free": data_json["is_free"] if "is_free" in data_json else None,
        "price_overview": data_json["price_overview"] if "price_overview" in data_json else None,
        "basegame_id": int(data_json["fullgame"]["appid"]) if "fullgame" in data_json else None,
        }
    return result

def get_steamprice():
    return