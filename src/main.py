#!/usr/bin/env python3
"""Main of the Program."""
import sys
from content.video import video_flux
from content.picture import check_pedestrian
from addons.arguments import treat_arguments
from room import Room
from api_com import get_code


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
        room.export_to_json()
    elif elm[0] == "api":
        return get_code(elm[2], display=True)
    else:
        pass
    return rtn_value


if __name__ == "__main__":
    sys.exit(main())
