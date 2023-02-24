"""Video mode of the program."""
from datetime import datetime
from time import sleep
from typing import Union
import cv2 as cv

from .api_com import get_available, report
from .room import Room, RoomErrors
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
        if cv.waitKey(1) in [ord("q"), 27]:
            print("Closing program.")
            break
        (img, b0, b1) = detect_pedestrian(frame, max_width=600, scale=1.05)
        if show:
            cv.putText(img, f'Il y a {b1} personnes avec potentiellement {b0 - b1} personnes de plus', (10, 30), cv.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255), 1, cv.LINE_AA)
            cv.imshow("Retour Video", img)
    cap.release()
    cv.destroyAllWindows()
    return rt_value

def video_flux_api(path: Union[str, int], adress: str, show: bool = True, bypass: bool = False) -> int:
    """This function launches a video and displays the humans.

    This is not final and might be cut later.
    """
    cap = cv.VideoCapture(path)
    rt_value = 0
    ret = True
    time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    room = Room()
    round_max = 20

    room.config_load()
    room.get_current_max_occupancy(get_available(adress, room.room_id, time), time)
    print(f"Waiting {room.time_wait}s until the room is open")

    if not cap.isOpened():
        print("Cannot open video flux.")
        rt_value = 84
    while cap.isOpened():
        if room.time_wait > 0 and bypass:
            sleep(room.time_wait)
            room.time_wait = 0
        time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        room.get_current_max_occupancy(get_available(adress, room.room_id, time), time)
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame. Exiting ...")
            break
        if cv.waitKey(room.update_time) in [ord("q"), 27]:
            print("Closing program.")
            break
        (img, b0, b1) = detect_pedestrian(frame, max_width=600, scale=1.05)
        room.current_occupancy += b1 + (b0 - b1) / 2
        if round_max <= 0:
            room.current_occupancy /= 20
            room.current_occupancy = int(room.current_occupancy)
            if room.get_room_status() != RoomErrors.NONE:
                report(adress, room.id, room.get_room_status())
                print(room.get_room_status())
            room.current_occupancy = 0
            round_max = 20
        round_max -= 1
        if show:
            cv.putText(img, f'Il y a {b1} personnes avec potentiellement {b0 - b1} personnes de plus', (10, 30), cv.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255), 1, cv.LINE_AA)
            cv.putText(img, f'Maximum {room.max_occupancy} personnes', (10, 60), cv.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255), 1, cv.LINE_AA)
            cv.imshow("Retour Video", img)
    cap.release()
    cv.destroyAllWindows()
    return rt_value