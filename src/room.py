"""Info fo room"""
import csv
import uuid
import datetime
from os.path import isfile
from enum import Enum


class RoomErrors(Enum):
    """Summary

    Args:
        Enum ([type]): [description]

    Returns:
        [type]: [description]
    """

    NONE = (0, "No errors")
    UNKNOWN = (1, "ISSUE: There is an issue with the Room")
    TOO_LOUD = (2, "ISSUE: Room as too much noise")
    TOO_MANY = (3, "FRAUD: There is currently too many people in the room")
    TOO_LITTLE = (
        4,
        "FRAUD: There is a negative amount of people (Might be an intruder)",
    )

    def __str__(self) -> str:
        """Summary

        Returns:
            str: [description]
        """
        if self.value[0] == 0:
            return "NO ERROR"
        return f"ERROR {self.value[0]}: '{self.value[1]}'"


class RoomStatus(Enum):
    """Summary

    Args:
        Enum ([type]): [description]
    """

    ADD_PEOPLE = 0
    REMOVE_PEOPLE = 1


class Room:
    """Summary

    Returns:
        [type]: [description]
    """

    room_id: uuid.UUID
    name: str = ""
    max_occupancy: int = 0
    currentOccupancy: int = 0
    volume_max: int = 0
    currentVolume: int = 0
    currentOccupants: list[str] = []
    supossedOccupants: list[str] = []

    def __init__(
        self,
        name: str = "Unnamed",
        max_occupancy: int = 1,
        room_id: uuid.UUID = uuid.uuid4(),
        volume_max: int = 70,
    ) -> None:
        """Summary

        Args:
            name (str, optional): [description]. Defaults to "Unnamed".
            max_occupancy (int, optional): [description]. Defaults to 1.
            room_id ([type], optional): [description]. Defaults to uuid.uuid4().
            volume_max (int, optional): [description]. Defaults to 70.
        """
        self.name = name
        self.room_id = room_id
        self.max_occupancy = max_occupancy
        self.volume_max = volume_max

    def __str__(self) -> str:
        """Summary

        Returns:
            str: [description]
        """
        return f"Name: '{self.name}', UUID: '{self.room_id}', Occupancy: {self.currentOccupancy}/{self.max_occupancy}, Volume: {self.currentVolume}/{self.volume_max} db, Time: {datetime.datetime.now().timestamp():.0f} UTC"

    @classmethod
    def remove_no_errors(self, elm: RoomErrors) -> bool:
        """Summary

        Args:
            elm (RoomErrors): [description]

        Returns:
            bool: [description]
        """
        if elm.value[0] == 0:
            return True
        return False

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

        self.currentVolume = volume
        if status == RoomStatus.ADD_PEOPLE:
            list_errors.append(self.get_new_occupants(amount))
        elif status == RoomStatus.REMOVE_PEOPLE:
            list_errors.append(self.get_new_occupants(amount))
        else:
            list_errors.append(RoomErrors.UNKNOWN)
        list_errors.append(self.get_room_status())
        filter(self.remove_no_errors, list_errors)
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
        fieldnames = ["date", "issue", "uuid", "number"]
        header = True
        if isfile(filename):
            with open(filename, mode="r") as csv_file:
                if csv_file.readable():
                    csv_reader = csv.reader(csv_file, delimiter=",")
                    firstLine = next(csv_reader)
                    if firstLine == fieldnames:
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
                        "uuid": self.currentOccupants,
                        "number": self.currentOccupancy,
                    }
                )

    @classmethod
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
        self.currentOccupants.extend(occupants)
        if len(occupants) != amount:
            return (RoomErrors.TOO_MANY, RoomErrors.TOO_LITTLE)[
                amount > self.currentOccupancy
            ]
        return RoomErrors.NONE

    @classmethod
    def get_supposed_occupants(self) -> None:
        """Summary"""
        # UPDATE AMOUNT
        self.supossedOccupants = []
        # UPDATE AMOUNT ENDED

    @classmethod
    def get_room_status(self) -> RoomErrors:
        """Summary

        Returns:
            RoomErrors: [description]
        """
        value = RoomErrors.NONE
        if self.currentOccupancy > self.max_occupancy:
            value = RoomErrors.TOO_MANY
        elif self.currentOccupancy < 0:
            value = RoomErrors.TOO_LITTLE
        elif self.currentVolume > self.volume_max:
            value = RoomErrors.TOO_LOUD
        return value


lol = Room()
print(lol)
lol.export_to_csv()
print(lol)
