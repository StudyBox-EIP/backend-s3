#!/usr/bin/env python3
from addons.arguments import treat_arguments
from cam.cam import camera
from vid.vid import video
from sys import argv


def main() -> int:
    """
    This function starts the program.
    """
    elm = treat_arguments(argv)

    if elm[0] == "cam":
        return camera()
    elif elm[0] == "vid":
        return video(elm[1])
    return 84


if __name__ == "__main__":
    exit(main())
