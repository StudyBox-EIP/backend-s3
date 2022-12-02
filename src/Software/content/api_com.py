"""Communicate with the server"""
from datetime import datetime
from typing import Any
import requests
import datetime

AUTH = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJhZG1pbkBzdHVkeWJveC5mciIsInBob25lIjpudWxsLCJyb2xlIjoiU3VwZXJBZG1pbiIsImZpcnN0X25hbWUiOiJkcXNkcXMiLCJsYXN0X25hbWUiOiJxc2Rxc2QiLCJhZ2UiOm51bGwsInByb21vIjpudWxsLCJjb25uZWN0ZWQiOmZhbHNlLCJhZGRyZXNzIjoiNjcgUnVlIFNhaW50LU1hdXIgNzUwMTEgUGFyaXMiLCJpbnN0aXR1dGlvbl9pZCI6bnVsbCwiZmF2b3JpdGVfcm9vbXMiOlsyLDVdLCJwcm9maWxfcGljdHVyZSI6MTQsImNyZWF0ZWRBdCI6IjIwMjItMTAtMjVUMTQ6MjU6NDYuNDgwWiIsInVwZGF0ZWRBdCI6IjIwMjItMTItMDFUMTM6NDg6MjAuNjE2WiIsImlhdCI6MTY2OTkxMDEwNywiZXhwIjoxNjcwNTE0OTA3fQ.tt124PnZh8HP6rloc0aRZsEtt6PJxEmfD5tkqXTd0fQ"

ROUTES = {
    "exist": (requests.get, "/"),
    "get_rooms": (requests.get, "/cameras"),
    "available": (requests.get, "/rooms/", "%ID", "/availability/", "%TIME"),
    "report": (requests.post, "/reports_auto/", "%ID"),
}


def handle_answer(response: requests.Response):
    """Returns the category of the error code

    Args:
        response (requests.Response): response from API

    Returns:
        int: Error code category
    """
    if response.status_code >= 500:
        print(f"Server error : {response.status_code}")
        return 5
    elif response.status_code >= 400:
        print(f"Client error : {response.status_code}")
        return 4
    elif response.status_code >= 300:
        print(f"Redirection : {response.status_code}")
        return 3
    elif response.status_code >= 200:
        print(f"Successful operation : {response.status_code}")
        return 2
    else:
        print(f"ERROR : IDK WEIRD CODE -> `{response.status_code}`")
        return 84


def fuse_route(route: str, room_id: Any, time: str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")):
    """Fuses the different element of a route

    Args:
        route (str): _description_
    """
    res = ""
    try:
        for k in ROUTES[route][1:]:
            if k == "%ID":
                res += str(room_id)
            elif k == "%TIME":
                res += time
            else:
                res += k
        return res
    except:
        return ""


def get_room(adress: str, cam_id: Any, route: str = "get_rooms") -> object:
    """_summary_

    Args:
        adress (str): _description_
        cam_id (Any): _description_
        route (str, optional): _description_. Defaults to "get_rooms".

    Returns:
        object: _description_
    """
    func = ROUTES[route][0]
    link = adress + fuse_route(route, cam_id)
    response = func(link)

    if handle_answer(response) != 2:
        return None
    for elm in response.json():
        if elm["id"] == cam_id:
            return elm["room_id"]
    return None

def get_available(adress: str, room_id: Any, time: str, route: str = "available") -> object:
    """_summary_

    Args:
        adress (str): _description_
        cam_id (Any): _description_
        route (str, optional): _description_. Defaults to "get_rooms".

    Returns:
        object: _description_
    """
    func = ROUTES[route][0]
    link = adress + fuse_route(route, room_id, time)
    response = func(link, headers={"Authorization": f"Bearer {AUTH}"})

    if handle_answer(response) != 2:
        return None
    return response.json()[0]

def report(
    adress: str,
    cam_id: int,
    issue: object,
    route: str = "report",
    display: bool = False,
) -> int:
    """_summary_

    Args:
        adress (str): Adress of the API
        cam_id (int): ID of the camera
        issue (object): Object with the report
        route (str, optional): is the wanted to route to acces. Defaults to "register".
        display (bool, optional): displays what the response is. Defaults to False.

    Returns:
        int: returns the first digit of the status code or 84 in case of unknown code
    """
    func = ROUTES[route][0]
    link = adress + fuse_route(route, cam_id)
    issue = {
        "date": datetime.datetime.now(),
        "desc": issue.get_txt(),
        "type": issue.get_code(),
    }
    response = func(link)
    if display:
        print(f"Data: {issue}")
        print(link)
        print(response.json())
    return handle_answer(response)
