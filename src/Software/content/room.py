"""Info fo room"""
import csv
import json
import datetime
from os.path import isfile
from os import getcwd
from enum import Enum
from typing import Any
from sys import stderr


class RoomErrors(Enum):
    """
    Summary

    Args:
        Enum ([type]): [description]

    Returns:
        [type]: [description]
    """

    NONE = (6, "No errors")
    UNKNOWN = (6, "ISSUE: There is an issue with the Room")
    TOO_LOUD = (1, "ISSUE: Room as too much noise")
    TOO_MANY = (2, "FRAUD: There is currently too many people in the room")
    TOO_LTL = (2, "FRAUD: There is a negative amount of people (Intruder)")

    def get_code(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return self.value[0]

    def get_txt(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return self.value[1]

    def __str__(self) -> str:
        """Summary

        Returns:
            str: [description]
        """
        if self.value[0] == 0:
            return "no error"
        return f"Error {self.value[0]}: '{self.value[1]}'"


class RoomStatus(Enum):
    """Summary

    Args:
        Enum ([type]): [description]
    """

    ADD_PEOPLE = 0
    REMOVE_PEOPLE = 1


def remove_no_errors(elm: RoomErrors) -> bool:
    """
    Summary

    Args:
        elm (RoomErrors): [description]

    Returns:
        bool: [description]
    """
    if elm.value[0] == 0:
        return True
    return False


class Room:
    """_summary_"""

    room_id: int = 0
    id: int = 0
    name: str = ""
    time_open: datetime.datetime = None
    time_close: datetime.datetime = None
    update_time: int = 1
    time_wait: int = 0
    max_occupancy: int = 0
    current_occupancy: float = 0.0
    max_volume: int = 0
    current_volume: int = 0
    current_occupants: list[str] = []
    supossed_occupants: list[str] = []

    def __init__(
        self,
        name: str = "Unnamed",
        cam_id: int = 0,
        room_id: int = 0,
        max_volume: int = 70,
    ):
        """Summary

        Args:
            name (str, optional): [description]. Defaults to "Unnamed".
            max_occupancy (int, optional): [description]. Defaults to 1.
            room_id ([type], optional): [description]. Defaults to uuid.uuid4().
            max_volume (int, optional): [description]. Defaults to 70.
        """
        self.name = name
        self.id = cam_id
        self.room_id = room_id
        self.max_volume = max_volume

    def __str__(self) -> str:
        """Summary.

        Returns:
            str: [description]
        """
        return f"Name: {self.id}-'{self.name}', Room ID: {self.room_id}, \
            Occupancy: {self.current_occupancy}/{self.max_occupancy}, \
            Volume: {self.current_volume}/{self.max_volume} db, \
            Time: {datetime.datetime.now().timestamp():.0f} UTC"

    def config_generate(self, filename: str = "config.json") -> None:
        """_summary_

        Args:
            file (str, optional): _description_. Defaults to "config.json".
        """
        with open(filename, mode="w") as json_file:
            data = {
                "id": self.room_id.__str__(),
                "name": self.name,
                "volume": self.max_volume,
                "room_id": self.max_occupancy,
            }
            json.dump(data, json_file, indent=4)
            print(f'Configuration file created at "{getcwd() + "/" + filename}"')

    def update_info_from_server(self, data: object):
        self.max_occupancy = data["seats_total"]
        self.time_open = datetime.datetime.strptime(
            data["open_hours"][0]["hour_start"], "%Y-%m-%dT%H:%M:%S.000Z"
        )
        self.time_close = datetime.datetime.strptime(
            data["open_hours"][-1]["hour_end"], "%Y-%m-%dT%H:%M:%S.000Z"
        )

    def get_current_max_occupancy(self, data: object, time: str):
        for timezone in data["open_hours"]:
            if (
                datetime.datetime.strptime(
                    timezone["hour_start"], "%Y-%m-%dT%H:%M:%S.000Z"
                )
                <= datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.000Z")
                <= datetime.datetime.strptime(
                    timezone["hour_end"], "%Y-%m-%dT%H:%M:%S.000Z"
                )
            ):
                self.max_occupancy = data["seats_total"] - timezone["avaible_seat"]
                self.time_open = datetime.datetime.strptime(
                    timezone["hour_start"], "%Y-%m-%dT%H:%M:%S.000Z"
                )
                self.time_close = datetime.datetime.strptime(
                    timezone["hour_end"], "%Y-%m-%dT%H:%M:%S.000Z"
                )
        if self.max_occupancy == 0:
            if datetime.datetime.strptime(
                time, "%Y-%m-%dT%H:%M:%S.000Z"
            ) < datetime.datetime.strptime(
                data["open_hours"][0]["hour_start"], "%Y-%m-%dT%H:%M:%S.000Z"
            ):
                self.time_wait = (
                    datetime.datetime.strptime(data["open_hours"][0]["hour_start"], "%Y-%m-%dT%H:%M:%S.000Z")
                    - datetime.datetime.strptime(
                        time, "%Y-%m-%dT%H:%M:%S.000Z"
                    )
                ).total_seconds()
            elif datetime.datetime.strptime(
                time, "%Y-%m-%dT%H:%M:%S.000Z"
            ) > datetime.datetime.strptime(
                data["open_hours"][-1]["hour_end"], "%Y-%m-%dT%H:%M:%S.000Z"
            ):
                self.time_wait = 3600
            else:
                self.time_wait = 1800

    def get_when_to_load(self):
        value = (self.time_open - datetime.datetime.now()).total_seconds()
        return value if value > 0 else 0

    def config_load(self, filename: str = "config.json") -> None:
        """_summary_

        Args:
            file (str, optional): _description_. Defaults to "config.json".
        """
        if not isfile(filename):
            print("You don't have a configuration file yet.", file=stderr)
            return
        with open(filename, mode="r+") as json_file:
            data = json.loads(json_file.read())
            self.id = data["id"]
            self.room_id = data["room_id"]
            self.name = data["name"]
            self.max_volume = data["volume"]

    def update_room_status(
        self, status: RoomStatus, amount: int, volume: int
    ) -> tuple[float, list[RoomErrors]]:
        """Summary

        Args:
            status (RoomStatus): [description]
            amount (int): [description]
            volume (int): [description]

        Returns:
            tuple[float, list[RoomErrors]]: [description]
        """

        errors: tuple[float, list[RoomErrors]] = (
            datetime.datetime.now().timestamp(),
            [],
        )
        list_errors = []

        self.current_volume = volume
        if status == RoomStatus.ADD_PEOPLE:
            list_errors.append(self.get_new_occupants(amount))
        elif status == RoomStatus.REMOVE_PEOPLE:
            list_errors.append(self.get_new_occupants(amount))
        else:
            list_errors.append(RoomErrors.UNKNOWN)
        list_errors.append(self.get_room_status())
        filter(remove_no_errors, list_errors)
        errors[1].extend(list_errors)
        return errors

    def export_to_csv(
        self,
        errors: tuple[float, list[RoomErrors]] = (
            datetime.datetime.now().timestamp(),
            [RoomErrors.NONE],
        ),
    ) -> None:
        """Summary

        Args:
            errors (tuple[float, list[RoomErrors]], optional): [description].
            Defaults to ( datetime.datetime.now().timestamp(), [RoomErrors.NONE], ).
        """
        filename = datetime.datetime.today().strftime("%Hh-%d-%m-%Y-info.csv")
        fieldnames = ["date", "issue", "uuid", "occupancy"]
        header = True
        if isfile(filename):
            with open(filename, mode="r") as csv_file:
                if csv_file.readable():
                    csv_reader = csv.reader(csv_file, delimiter=",")
                    first_line = next(csv_reader)
                    if first_line == fieldnames:
                        header = False
        with open(filename, mode="a") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if header:
                writer.writeheader()
            for error in errors[1]:
                writer.writerow(
                    {
                        "date": errors[0],
                        "issue": str(error),
                        "uuid": self.current_occupants,
                        "occupancy": self.current_occupancy,
                    }
                )

    def export_to_json(
        self,
        errors: tuple[float, list[RoomErrors]] = (
            datetime.datetime.now().timestamp(),
            [RoomErrors.NONE],
        ),
    ) -> None:
        """Summary

        Args:
            errors (tuple[float, list[RoomErrors]], optional): [description].
            Defaults to ( datetime.datetime.now().timestamp(), [RoomErrors.NONE], ).
        """
        filename = datetime.datetime.today().strftime("%Hh-%d-%m-%Y-info.json")
        error_list: Any = []
        if not isfile(filename):
            with open(filename, mode="w") as json_file:
                data = {
                    "room_id": self.room_id.__str__(),
                    "name": self.name,
                    "occupancy": self.max_occupancy,
                    "volume": self.max_volume,
                    "errors": [],
                }
                for error in errors[1]:
                    error_list.append(
                        {
                            "time": errors[0],
                            "issue": str(error),
                            "users": self.current_occupants,
                            "occupancy": self.current_occupancy,
                        }
                    )
                data["errors"] = error_list
                json.dump(data, json_file, indent=4)
        else:
            with open(filename, mode="r+") as json_file:
                data = json.loads(json_file.read())
                error_list = data["errors"]
                for error in errors[1]:
                    error_list.append(
                        {
                            "time": errors[0],
                            "issue": str(error),
                            "users": self.current_occupants,
                            "occupancy": self.current_occupancy,
                        }
                    )
                data["errors"] = error_list
                json_file.seek(0)
                json.dump(data, json_file, indent=4)

    def get_new_occupants(self, amount: int) -> RoomErrors:
        """Summary

        Args:
            amount (int): [description]

        Returns:
            RoomErrors: [description]
        """
        # UPDATE AMOUNT
        occupants: list[str] = []
        # UPDATE AMOUNT ENDED
        self.current_occupants.extend(occupants)
        if len(occupants) != amount:
            return (RoomErrors.TOO_MANY, RoomErrors.TOO_LTL)[
                amount > self.current_occupancy
            ]
        return RoomErrors.NONE

    def get_room_status(self) -> RoomErrors:
        """Summary

        Returns:
            RoomErrors: [description]
        """
        value = RoomErrors.NONE
        if self.current_occupancy > self.max_occupancy:
            value = RoomErrors.TOO_MANY
        elif self.current_occupancy < 0:
            value = RoomErrors.TOO_LTL
        elif self.current_volume > self.max_volume:
            value = RoomErrors.TOO_LOUD
        return value
