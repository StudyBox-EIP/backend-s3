"""Communicate with the server"""
import requests

AUTH = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJhZG1pbkBzdHVkeWJveC5mciIsInBob25lIjpudWxsLCJyb2xlIjoiU3VwZXJBZG1pbiIsImZpcnN0X25hbWUiOm51bGwsImxhc3RfbmFtZSI6bnVsbCwiYWdlIjpudWxsLCJwcm9tbyI6bnVsbCwiY29ubmVjdGVkIjpmYWxzZSwiaW5zdGl0dXRpb25faWQiOm51bGwsImNyZWF0ZWRBdCI6IjIwMjItMDYtMjNUMTE6MTM6MjAuMzM0WiIsInVwZGF0ZWRBdCI6IjIwMjItMDYtMjNUMTE6MTM6MjAuMzM0WiIsImlhdCI6MTY1NjAxMzc3OCwiZXhwIjoxNjU2NjE4NTc4fQ.6PnKNvMgwh9GLmy0ZBEHqeWjQOFdntW84Br99qm7zo0"

ROUTES = {
    "exist": (requests.get, "/"),
    "get_rooms": (requests.get, "/rooms"),
    "current_room": (requests.get, "/camera/", "%ID", "/room"),
    "register": (requests.post, "/camera/register"),
    "report": (requests.post, "/report_auto/", "%ID"),
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


def fuse_route(route: str, room_id: str):
    """Fuses the different element of a route

    Args:
        route (str): _description_
    """
    res = ""
    for k in ROUTES[route][1:]:
        if k == "#ID":
            res += room_id
        else:
            res += k
    return res


def get_code(
    adress: str, room_id: str, route: str = "exist", display: bool = False
) -> int:
    """This function returns the code status of the request asked.

    Args:
        room_id (str): ID of the Camera
        adress (str): is the adress of the website
        route (str, optional): is the wanted to route to acces. Defaults to "exist".
        display (bool, optional): displays what the response is. Defaults to False.

    Returns:
        int: returns the first digit of the status code or 84 in case of unknown code
    """
    func = ROUTES[route][0]
    link = adress + fuse_route(route, room_id)
    response = func(link, headers={"Authorization": "Bearer " + AUTH})
    if display:
        print(link)
        print(response.json())
    return handle_answer(response)


def register(
    adress: str,
    room_id: str,
    route: str = "register",
    name: str = "Basic Camera 01",
    volume: float = 70,
    display: bool = False,
) -> int:
    """Registers the current camera to the server

    Args:
        adress (str): Adress of the API
        room_id (str): ID of the room
        route (str, optional): is the wanted to route to acces. Defaults to "register".
        name (str, optional): Name of the Camera. Defaults to "Basic Camera 01".
        volume (float, optional): Volume max for the room. Defaults to 70.
        display (bool, optional): displays what the response is. Defaults to False.

    Returns:
        int: returns the first digit of the status code or 84 in case of unknown code
    """
    func = ROUTES[route][0]
    link = adress + fuse_route(route, room_id)
    response = func(
        link, data={"id_salle": room_id, "name": name, "volume_max": volume}
    )
    if display:
        print(link)
        print(response.json())
    return handle_answer(response)


def report(
    adress: str,
    room_id: str,
    issue: object,
    route: str = "report",
    display: bool = False,
) -> int:
    """_summary_

    Args:
        adress (str): Adress of the API
        room_id (str): ID of the camera
        issue (object): Object with the report
        route (str, optional): is the wanted to route to acces. Defaults to "register".
        display (bool, optional): displays what the response is. Defaults to False.

    Returns:
        int: returns the first digit of the status code or 84 in case of unknown code
    """
    func = ROUTES[route][0]
    link = adress + fuse_route(route, room_id)
    # {"date": , "desc": , "report_type_id": }
    response = func(link, data=issue)
    if display:
        print(link)
        print(response.json())
    return handle_answer(response)
