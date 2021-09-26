import pytest
import typing
import cv2 as cv


def test_dependence_good() -> None:
    capture = cv.VideoCapture("assets/videos/rabbit.mp4")
    assert capture.isOpened()
    capture.release()
