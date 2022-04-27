"""detect"""
from typing import Any
import imutils
import cv2 as cv


def detect_pedestrian(
    origin_img: Any,
    max_width: int = 600,
    scale: float = 1.22,
    weight: float = 0.35,
) -> tuple[Any, int, int]:
    """[summary]

    Args:
        origin_img (Any): [description]
        max_width (int, optional): [description]. Defaults to 600.
        scale (float, optional): [description]. Defaults to 1.22.
        weight (float, optional): [description]. Defaults to 0.35.

    Returns:
        [type]: [description]
    """
    origin = imutils.resize(origin_img, width=min(max_width, origin_img.shape[1]))
    img = origin.copy()
    boxes = [0, 0]
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    hog = cv.HOGDescriptor()
    hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
    rects, weights = hog.detectMultiScale(
        gray, winStride=(4, 4), padding=(8, 8), scale=scale
    )
    for (x_p, y_p, w_b, h_b) in rects:
        if weights[boxes[0]] >= weight:
            boxes[1] += 1
            cv.rectangle(img, (x_p, y_p), (x_p + w_b, y_p + h_b), (0, 255, 0), 2)
        boxes[0] += 1
    return (img, boxes[0], boxes[1])
