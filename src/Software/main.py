#!/usr/bin/env python3
"""Main of the Program."""
import sys
from time import sleep
from content.video import video_flux, video_flux_api
from content.picture import check_pedestrian
from addons.arguments import treat_arguments
from content.room import Room
from content.api_com import get_available, get_room, report
from datetime import datetime

def main() -> int:
    """Starts the program

    Returns:
        int: Status of the program
    """
    elm = treat_arguments(sys.argv)
    rtn_value = 84

    if elm[0] == "vid":
        rtn_value = video_flux_api(elm[1], elm[2])
    elif elm[0] == "cam":
        rtn_value = video_flux_api(elm[5], elm[2])
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
        time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        room = Room()
        room.config_load()
        room.get_current_max_occupancy(get_available(elm[2], room.room_id, time), time)
        print(f"Waiting {room.time_wait}s until the room is open")
        room.update_time = 1
        while True:
            if room.time_wait > 0:
                sleep(room.time_wait)
                room.time_wait = 0
            room.get_current_max_occupancy(get_available(elm[2], room.room_id, time), time)
            time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
            print(room.get_room_status())
            sleep(room.update_time)
    else:
        pass
    return rtn_value


if __name__ == "__main__":
    sys.exit(main())
