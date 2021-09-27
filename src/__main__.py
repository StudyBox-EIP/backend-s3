#!/usr/bin/env python3
"""Main of the Program."""
import sys
from cam.cam import camera
from vid.vid import video
from addons.arguments import treat_arguments


def main() -> int:
    """
    This function starts the program.
    """
    elm = treat_arguments(sys.argv)

    if elm[0] == "vid":
        return video(elm[1])
    return camera()


if __name__ == "__main__":
    sys.exit(main())
