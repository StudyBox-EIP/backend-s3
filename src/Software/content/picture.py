"""Picture mode of the program."""
from imutils import paths
import cv2 as cv
from .detect import detect_pedestrian


def check_pedestrian(wait_time: int = 0, show: bool = True) -> int:
    """This is the check for pedestrian trough a folder of pictures.

    This is an independent part of the code.
    """
    hog = cv.HOGDescriptor()
    hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

    for image_path in paths.list_images("assets/pictures"):
        orig = cv.imread(image_path)
        image = orig.copy()
        image, origin, correc = detect_pedestrian(
            orig, max_width=400, scale=1.05, weight=0.65
        )
        filename = image_path[image_path.rfind("/") + 1 :]
        print(f"[INFO] {filename}: {origin} boite d'origne, {correc} apres correction")
        if show:
            cv.imshow("Apres NMS", image)
        cv.waitKey(wait_time)
    return 0
