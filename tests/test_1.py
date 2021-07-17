import pytest
import typing
import cv2 as cv


def test_dependence_good() -> None:
    capture = cv.VideoCapture("./video/SampleVideo_1280x720_1mb.mp4")
    assert capture.isOpened()
    capture.release()
