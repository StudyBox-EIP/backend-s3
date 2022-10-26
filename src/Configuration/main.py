#!/usr/bin/env python3
"""Main of the Program."""
from sqlite3 import connect
import sys
import json
import tkinter as tk
from tkinter import LEFT, ttk, messagebox
from os import getcwd
import requests

window = tk.Tk()
room_name = tk.StringVar()
room_uuid = tk.IntVar()
room_volume = tk.IntVar()
login = tk.StringVar()
password = tk.StringVar()
server_dev = tk.BooleanVar()


def config_generate() -> None:
    """_summary_
    """
    with open("config.json", mode="w") as json_file:
        data = {
            "name": room_name.get(),
            "volume": room_volume.get(),
            "room_id": room_uuid.get(),
        }
        json.dump(data, json_file, indent=4)
        print(f'Configuration file created at "{getcwd() + "/config.json"}"')
        messagebox.showinfo("File Success", f'Configuration file created at "{getcwd() + "/config.json"}".')

def send_to_server() -> None:
    """_summary_
    """
    address = "https://dev.api.studybox.fr" if server_dev.get() else "https://api.studybox.fr"
    answer = requests.post(address + "/cameras", data={"name": room_name.get(), "volume": room_volume.get(), "room_id": room_uuid.get()})
    txt = answer.json()

    if answer.status_code != 201:
        messagebox.showerror("Server Issue", txt["message"])
        return
    messagebox.showinfo("Server Success", f'The camera has been set on the server. It has the ID {txt["id"]}. It is connected to room id{txt["room_id"]["id"]} - {txt["room_id"]["name"]}.')
    print(f'The camera has been set on the server. It has the ID {txt["id"]}. It is connected to room id{txt["room_id"]["id"]} - {txt["room_id"]["name"]}.')


def generate_and_send() -> None:
    """_summary_
    """
    config_generate()
    send_to_server()

def main() -> int:
    # Info
    window.title("Configuration Room")
    # Elm Variable
    room_name.set("None")
    room_uuid.set(0)
    room_volume.set(60)
    server_dev.set(False)
    login.set("admin@studybox.fr")
    password.set("AArnMPmbJFMY4xBgxF$1")
    # Elements
    elm_pack = tk.Frame(window)
    elm_pack.pack(padx=8, pady=8)

    rnt = tk.Label(elm_pack, text="Camera Name")
    rnt.pack()
    rne = tk.Entry(elm_pack, textvariable=room_name)
    rne.pack()
    rut = tk.Label(elm_pack, text="Room UUID")
    rut.pack()
    rue = tk.Entry(elm_pack, textvariable=room_uuid)
    rue.pack()

    rvt = tk.Label(elm_pack, text="Room Volume")
    rvt.pack()
    rvs = tk.Scale(
        elm_pack, orient=tk.HORIZONTAL, from_=40, to=120, showvalue=True, variable=room_volume
    )
    rvs.pack()

    # Separator
    sep = ttk.Separator(window,orient='horizontal')
    sep.pack(fill='x', padx=8)

    # Admin Login
    adm_pack = tk.Frame(window)
    adm_pack.pack(padx=8, pady=8)

    ondev = tk.Checkbutton(adm_pack, text='On DEV Server', variable=server_dev)
    ondev.pack()

    # Separator
    sep = ttk.Separator(window,orient='horizontal')
    sep.pack(fill='x', padx=8)

    # Buttons

    bt_pack = tk.Frame(window)
    bt_pack.pack(padx=8, pady=(8, 0))

    gt = tk.Button(bt_pack, text="Generate", background="#55FF55", command=config_generate)
    gt.pack(side=LEFT)

    sts = tk.Button(bt_pack, text="Send to Server", background="#55FF55", command=send_to_server)
    sts.pack(side=LEFT)


    gas = tk.Button(text="Generate & Send to Server", background="#55FF55", command=generate_and_send)
    gas.pack(pady=(0, 8))

    # Loop
    window.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
