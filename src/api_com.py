"""Communicate with the server"""
import requests

ROUTES = {
    "exist": ("/", requests.get),
    "get_room": ("/rooms", requests.get),
    "post_abus": ("/base", requests.get),
}


def get_code(adress: str, route: str = "exist", display: bool = False) -> int:
    """This function returns the code status of the request asked.

    Args:
        adress (str): is the adress of the website
        route (str, optional): is the wanted to route to acces. Defaults to "exist".
        display (bool, optional): displays what the response is. Defaults to False.

    Returns:
        int: returns the first digit of the status code or 84 in case of unknown code
    """
    func = ROUTES[route][1]
    link = adress + str(ROUTES[route][0])
    response = func(link)

    if display:
        print(link)
        print(response.json())

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
