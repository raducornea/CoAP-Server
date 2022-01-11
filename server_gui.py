from tkinter import *
from tkinter import messagebox
import file_system as fs  # circular import error prevention
import server_logic as server
import threading


class GUI:
    thread = threading.Thread(target=server.Logic.server_start)
    window = None
    button_start = None
    button_stop = None
    button_clear = None
    button_exit = None
    text_box = None

    @classmethod
    def __init__(cls):
        # window root
        cls.window = Tk()

        # button widgets
        cls.button_start = Button(cls.window,
                                  height=3,
                                  width=10,
                                  text="Start Server",
                                  font="arial 15 bold",
                                  bg="cyan",
                                  pady=20,
                                  command=cls.start_server)
        cls.button_stop = Button(cls.window,
                                 height=3,
                                 width=10,
                                 text="Stop Server",
                                 font="arial 15 bold",
                                 bg="cyan",
                                 pady=20,
                                 command=cls.close_server)
        cls.button_clear = Button(cls.window,
                                  height=3,
                                  width=10,
                                  text="Clear Screen",
                                  font="arial 15 bold",
                                  bg="cyan",
                                  pady=20,
                                  command=cls.clear_screen)
        cls.button_exit = Button(cls.window,
                                 height=3,
                                 width=10,
                                 text="Exit",
                                 font="arial 15 bold",
                                 bg="cyan",
                                 pady=20,
                                 command=cls.exit_application)

        # text widgets
        cls.text_box = Text(cls.window,
                            height=25,
                            width=66,
                            font="arial 10",
                            bg="white")

    # attempt to start the server
    @classmethod
    def start_server(cls):
        # Start Server on a new Thread
        server.Logic.__init__()
        cls.thread = threading.Thread(target=server.Logic.server_start)
        cls.thread.start()

        print('--Starting Server')
        cls.button_start.place_forget()
        cls.button_stop.place(x=468, y=0)
        cls.text_box.place(x=0, y=0)

        cls.print_message("Server is On!")

        # sets file system to absolute path
        fs.FileSystem.__init__()

    # attempt to close the server
    @classmethod
    def close_server(cls):
        server.Logic.server_stop()

        print('--Closing Server')
        cls.button_stop.place_forget()
        cls.button_start.place(x=468, y=0)
        cls.print_message("Server is Off!")

    # terminate application execution
    @classmethod
    def exit_application(cls):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            server.Logic.server_stop()

            print('--Exiting Application')
            cls.window.destroy()

    # clears the screen with a button
    @classmethod
    def clear_screen(cls):
        print('--Clearing Screen')
        cls.text_box.config(state=NORMAL)
        cls.text_box.delete(1.0, "end")
        cls.text_box.config(state=DISABLED)

    # print messages to the text box
    # prevents user from typing random stuff in the box
    @classmethod
    def print_message(cls, message):
        cls.text_box.config(state=NORMAL)
        cls.text_box.insert(END, ">> " + message + "\n")  # 1.0 insereaza la inceput / END insereaza la sfarsit
        cls.text_box.config(state=DISABLED)

    # todo
    #  remove and use print_message everywhere
    @classmethod
    def console(cls, message):
        cls.console_message = message

    # open the application when running main
    @classmethod
    def open_application(cls):
        cls.console_message = ''

        # set window attributes
        cls.window.geometry("600x400")
        cls.window.resizable(0, 0)
        cls.window.title('FS Browser - Server')

        # position widgets
        cls.button_start.place(x=468, y=0)
        cls.button_clear.place(x=468, y=133)
        cls.button_exit.place(x=468, y=266)
        cls.text_box.place(x=0, y=0)

        # friendly message helper
        cls.print_message("Welcome to the Server Interface!\n"
                          ">> To browse the File System, use the Client and type os commands like 'cwd'!")

        # x button messagebox and function
        cls.window.protocol("WM_DELETE_WINDOW", cls.exit_application)

        # loop the application
        cls.window.mainloop()
