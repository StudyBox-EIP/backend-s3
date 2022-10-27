#!/usr/bin/env python3
"""Main of the Program."""
import sys
from time import sleep
from content.video import video_flux
from content.picture import check_pedestrian
from addons.arguments import treat_arguments
from room import Room
from api_com import get_room, report


def main() -> int:
    """Starts the program

    Returns:
        int: Status of the program
    """
    elm = treat_arguments(sys.argv)
    rtn_value = 84

    if elm[0] == "vid":
        rtn_value = video_flux(elm[1])
    elif elm[0] == "cam":
        rtn_value = video_flux(0)
    elif elm[0] == "img":
        rtn_value = check_pedestrian()
    elif elm[0] == "room":
        room = Room()
        if elm[4]:
            room.config_generate(elm[3] + ".json")
        else:
            room.config_load(elm[3] + ".json")
        print(room)
        room.export_to_json()
    elif elm[0] == "api":
        room = Room()
        room.config_load()
        room.update_info_from_server(get_room(elm[2], room.id))
        print(f"Waiting {room.get_when_to_load()}s until the room is open")
        sleep(room.get_when_to_load())
        maxi = 10
        while maxi:
            rtn_value = report(elm[2], room.id, room.get_room_status())
            sleep(room.time_wait)
            maxi -= 1
    else:
        pass
    return rtn_value


if __name__ == "__main__":
    sys.exit(main())
