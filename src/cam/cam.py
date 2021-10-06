"""Camera mode of the program."""
import cv2 as cv


def camera() -> int:
    """This function launches your camera and displays the humans.

    This is not final and might be cut later.
    """
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
