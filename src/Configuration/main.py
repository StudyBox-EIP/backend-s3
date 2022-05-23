#!/usr/bin/env python3
"""Main of the Program."""
import sys
import json
import tkinter as tk
from os import getcwd

window = tk.Tk()


room_name = tk.StringVar()
room_uuid = tk.StringVar()
room_volume = tk.IntVar()
room_occupancy = tk.IntVar()


def config_generate() -> None:
    """_summary_

    Args:
        file (str, optional): _description_. Defaults to "config.json".
    """
    with open("config.json", mode="w") as json_file:
        data = {
            "uuid": room_uuid.get(),
            "name": room_name.get(),
            "volume": room_volume.get(),
            "occupancy": room_occupancy.get(),
        }
        json.dump(data, json_file, indent=4)
        print(f'Configuration file created at "{getcwd() + "/config.json"}"')


def main() -> int:
    # Info
    window.title("Configuration Room")
    # Elm Variable
    room_name.set("None")
    room_uuid.set("xxx")
    room_volume.set(60)
    room_occupancy.set(10)
    # Elements
    rnt = tk.Label(text="Room Name")
    rnt.pack()
    rne = tk.Entry(textvariable=room_name)
    rne.pack()
    rut = tk.Label(text="Room UUID")
    rut.pack()
    rue = tk.Entry(textvariable=room_uuid)
    rue.pack()

    rvt = tk.Label(text="Room Volume")
    rvt.pack()
    rvs = tk.Scale(
        orient=tk.HORIZONTAL, from_=40, to=120, showvalue=True, variable=room_volume
    )
    rvs.pack()

    rot = tk.Label(text="Room Occupancy")
    rot.pack()
    ros = tk.Scale(
        orient=tk.HORIZONTAL, from_=5, to=30, showvalue=True, variable=room_occupancy
    )
    ros.pack()

    gt = tk.Button(text="Generate", background="#55FF55", command=config_generate)
    gt.pack()
    # Loop
    window.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
