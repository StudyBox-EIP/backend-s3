"""Video mode of the program."""
import cv2 as cv


def video(path: str) -> int:
    """This function launches a video and displays the humans.

    This is not final and might be cut later.
    """
    cap = cv.VideoCapture(path)
    rt_value = 84

    if cap.isOpened():
        rt_value = 0
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
    return rt_value
