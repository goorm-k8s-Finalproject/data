"""
steam api를 호출하여 app의 상세 정보를 불러오는 모듈
"""
import requests
import json

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
    appdetail_get = requests.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=KRW&l=koreana")
    detail_json = json.loads(appdetail_get.text)
    if detail_json[f"{app_id}"]["success"] == False:
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
        "short_decription": data_json["short_description"] if "short_description" in data_json else None,
        "pc_requirements": data_json["pc_requirements"] if "pc_requirements" in data_json else None,
        }
    return result

def get_steamprice():
    return