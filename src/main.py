#!/usr/bin/env python3
import numpy as np
import cv2 as cv
from sys import argv
from typing import List
from os.path import exists


def video(path: str):
    cap = cv.VideoCapture(path)
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow("frame", gray)
        if cv.waitKey(1) == ord("q"):
            break
    cap.release()
    cv.destroyAllWindows()
    return 0


def camera():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return 84
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Display the resulting frame
        cv.imshow("frame", gray)
        if cv.waitKey(1) == ord("q"):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()
    return 0


def main(n: int, args: List[str]):
    if n == 2 and args[1] == "cam":
        return camera()
    elif n == 3 and args[1] == "vid" and exists(args[2]):
        return video(args[2])
    return 84


if __name__ == "__main__":
    exit(main(len(argv), argv))
