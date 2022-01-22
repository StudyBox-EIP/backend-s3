"""Camera mode of the program."""
import cv2 as cv


def camera(show: bool = True) -> int:
    """This function launches your camera and displays the humans.

    This is not final and might be cut later.
    """
    cap = cv.VideoCapture(0)
    rt_value = 0

    if not cap.isOpened():
        print("Cannot open camera")
        rt_value = 84
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        if show:
            cv.imshow("frame", gray)
        if cv.waitKey(1) == ord("q"):
            break
    cap.release()
    cv.destroyAllWindows()
    return rt_value
