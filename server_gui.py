import threading
from tkinter import *

import server_communication


class GUI:
    def __init__(self):
        self.window = Tk()

        # Cream butoanele
        self.button_start = Button(self.window,
                                   text="Start Server",
                                   font="arial 15 bold",
                                   bg="cyan",
                                   pady=20,
                                   command=self.start_server)
        self.button_stop = Button(self.window,
                                  text="Stop Server",
                                  font="arial 15 bold",
                                  bg="cyan",
                                  pady=20,
                                  command=self.close_server)
        self.communication = server_communication.Communication()
        self.thread = threading.Thread(target=self.communication.start_server)

    def start_server(self):
        self.communication = server_communication.Communication()

        self.button_start.place_forget()
        self.button_stop.place(x=250, y=130)

        self.thread = threading.Thread(target=self.communication.start_server)
        self.thread.start()

    def close_server(self):
        print('Closing Server')
        self.button_stop.place_forget()
        self.button_start.place(x=50, y=130)

        self.communication.close_server()

    def open_application(self):
        self.window.geometry("800x600")
        self.window.resizable(0, 0)
        self.window.title('File Server')

        # Pozitionam butonul
        self.button_start.place(x=50, y=130)

        self.window.mainloop()
