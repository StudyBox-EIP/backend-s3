"""Checks people in a set of data."""
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import imutils
import cv2


def check_pedestrian() -> int:
    """This is the check for pedestrian trough a folder of pictures.

    This is an independent part of the code.
    """
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    for image_path in paths.list_images("assets/pictures"):
        image = cv2.imread(image_path)
        image = imutils.resize(image, width=min(400, image.shape[1]))
        orig = image.copy()
        (rects, _) = hog.detectMultiScale(
            image, winStride=(4, 4), padding=(8, 8), scale=1.05
        )
        for (x, y, w, h) in rects:
            cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
        filename = image_path[image_path.rfind("/") + 1 :]
        print(
            f"[INFO] {filename}: {len(rects)} boite d'origne, {len(pick)} apres correction"
        )
        cv2.imshow("Avant NMS", orig)
        cv2.imshow("Apres NMS", image)
        cv2.waitKey(0)
    return 0
