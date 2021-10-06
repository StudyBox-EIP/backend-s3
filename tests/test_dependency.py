import pytest

# Dependency
import cv2 as cv
from argparse import ArgumentParser, ArgumentError


def test_opencv_open() -> None:
    capture = cv.VideoCapture("assets/videos/rabbit.mp4")
    assert capture.isOpened()
    capture.release()


def test_argparse_create_parser() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "type",
        type=str,
        choices=["cam", "vid"],
        help="this is the type of use wanted for the program",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="",
        help="this is the video used by the 'vid' type",
    )
    try:
        parser.parse_args(["cam"])
    except ArgumentError:
        assert False
    assert True
