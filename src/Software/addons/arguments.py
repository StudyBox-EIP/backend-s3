"""Gets the input for the program."""
from typing import Tuple, List
from argparse import ArgumentParser, ArgumentError
from os.path import isfile
import sys

# Default video when 'vid' type is selected
DEFAULT_VIDEO = "assets/videos/chalais_cinema_long.mp4"


# This is all format video accepted by the program
VIDEO_FORMAT = [".mp4", ".m4a"]

# Adress of studybox
DEV_API = "https://dev.api.studybox.fr"
PROD_API = "https://api.studybox.fr"

#
DEFAULT_CONFIG_FILE = "config"


def parse_arguments(arguments: List[str]) -> Tuple[str, str, str, str, bool, int]:
    """This fonction parses all the arguments and takes care of the help display.

    This returns a tuple of all the wanted arguement.
    It should takes 'argv' without the first element.
    """
    parser = ArgumentParser()
    parser.add_argument(
        "type",
        type=str,
        choices=["cam", "vid", "img", "api", "room"],
        help="this is the type of use wanted for the program",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default=DEFAULT_VIDEO,
        help="this is the video used by the 'vid' type",
    )
    parser.add_argument(
        "-d",
        "--dev",
        action="store_const",
        const=DEV_API,
        default=PROD_API,
        help="can be added to change API from production to dev",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="this is the config file for the room",
    )
    parser.add_argument(
        "-g",
        "--generate",
        action="store_const",
        const=True,
        default=False,
        help="this generates a config file for the room",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=int,
        default=0,
        help="this tells the system wich camera to use",
    )
    try:
        args = parser.parse_args(arguments)
    except ArgumentError:
        parser.print_help()
        sys.exit(84)
    return (args.type, args.file, args.dev, args.config, args.generate, args.input)


def treat_arguments(args: List[str]) -> Tuple[str, str, str, str, bool]:
    """This takes in all the argument wanted an treats them.

    This returns a Tuple with the functionment type and the adress of a video file.
    This function sys.exits when a parameter is not right or as an issue.
    """
    parse = parse_arguments(args[1:])

    if parse[0] == "vid":
        if not isfile(parse[1]):
            print("Adress given is not a file or doesn't exist.", file=sys.stderr)
            sys.exit(84)
        if not parse[1][-4:] in VIDEO_FORMAT:
            print("This file is not in an accepted format.", file=sys.stderr)
            print(f"The accepted format are : {VIDEO_FORMAT}", file=sys.stderr)
            sys.exit(84)
    if parse[0] == "room" and parse[3] is None and not parse[4]:
        print("Adress given is not a file or doesn't exist.", file=sys.stderr)
        sys.exit(84)
    if parse[3] is None:
        return (parse[0], parse[1], parse[2], DEFAULT_CONFIG_FILE, parse[4], parse[5])
    return (parse[0], parse[1], parse[2], parse[3], parse[4], parse[5])
