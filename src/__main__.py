#!/usr/bin/env python3
"""Main of the Program."""
import sys
from cam.cam import camera
from vid.vid import video
from check_pictures import check_pedestrian
from addons.arguments import treat_arguments


def main() -> int:
    """This function starts the program."""
    elm = treat_arguments(sys.argv)
    rtn_value = 84

    if elm[0] == "vid":
        rtn_value = video(elm[1])
    elif elm[0] == "cam":
        rtn_value = camera()
    else:
        rtn_value = check_pedestrian()
    return rtn_value


if __name__ == "__main__":
    sys.exit(main())
