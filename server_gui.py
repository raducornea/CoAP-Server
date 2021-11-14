from tkinter import *
from tkinter import ttk
from threading import *

from server_communication import start_server as start
from server_communication import close_server as stop
from server_communication import communicate


def start_server():
    global button_start, button_stop, thread

    button_start.place_forget()
    button_stop.place(x=250, y=130)

    start()
    thread = Thread(target=communicate)
    thread.start()


def stop_server():
    global button_start, button_stop, thread

    button_stop.place_forget()
    button_start.place(x=50, y=130)

    stop()
    thread = Thread(target=communicate)
    thread.start()


def start_application():
    global button_start, button_stop, thread

    window = Tk()
    window.geometry("800x600")
    window.resizable(0, 0)
    window.title('File Server')

    # Cream butoanele
    button_start = Button(window,
                          text="Start Server",
                          font="arial 15 bold",
                          bg="cyan",
                          pady=20,
                          command=start_server)
    button_stop = Button(window,
                         text="Stop Server",
                         font="arial 15 bold",
                         bg="cyan",
                         pady=20,
                         command=stop_server)

    # Pozitionam butoanele - e mult mai bine sa le dam .place DUPA si nu odata cu crearea lor,
    # tocmai pentru ca nu poti folosi command=lambda: b.place_forget()
    button_start.place(x=50, y=130)

    window.mainloop()
