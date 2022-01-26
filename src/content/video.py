"""Video mode of the program."""
from typing import Union
import cv2 as cv
from .detect import detect_pedestrian


def video_flux(path: Union[str, int], show: bool = True) -> int:
    """This function launches a video and displays the humans.

    This is not final and might be cut later.
    """
    cap = cv.VideoCapture(path)
    rt_value = 0
    ret = True

    if not cap.isOpened():
        print("Cannot open video flux.")
        rt_value = 84
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame. Exiting ...")
            break
        if cv.waitKey(1) == ord("q"):
            print("Closing program.")
            break
        (img, _, _) = detect_pedestrian(frame, max_width=600, scale=1.05)
        if show:
            cv.imshow("frame", img)
    cap.release()
    cv.destroyAllWindows()
    return rt_value
