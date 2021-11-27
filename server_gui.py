from tkinter import *
import file_system as fs  # circular import error prevention


class GUI:
    console_message = ''

    def __init__(self):
        # window root
        self.window = Tk()

        # button widgets
        self.button_start = Button(self.window,
                                   height=3,
                                   width=10,
                                   text="Start Server",
                                   font="arial 15 bold",
                                   bg="cyan",
                                   pady=20,
                                   command=self.start_server)
        self.button_stop = Button(self.window,
                                  height=3,
                                  width=10,
                                  text="Stop Server",
                                  font="arial 15 bold",
                                  bg="cyan",
                                  pady=20,
                                  command=self.close_server)
        self.button_clear = Button(self.window,
                                   height=3,
                                   width=10,
                                   text="Clear Screen",
                                   font="arial 15 bold",
                                   bg="cyan",
                                   pady=20,
                                   command=self.clear_screen)
        self.button_exit = Button(self.window,
                                  height=3,
                                  width=10,
                                  text="Exit",
                                  font="arial 15 bold",
                                  bg="cyan",
                                  pady=20,
                                  command=self.exit_application)

        # text widgets
        self.text_box = Text(self.window,
                             height=25,
                             width=66,
                             font="arial 10",
                             bg="white")

        # self.communication = server_communication.Communication()
        # self.thread = threading.Thread(target=self.communication.start_server)

    # attempt to start the server
    def start_server(self):
        # self.communication = server_communication.Communication()

        print('--Starting Server')
        self.button_start.place_forget()
        self.button_stop.place(x=468, y=0)
        self.text_box.place(x=0, y=0)

        self.print_message("Server is On!")

        fs.FileSystem.__init__()
        fs.FileSystem.get_current_work_directory()

        fs.FileSystem.new_file()
        fs.FileSystem.new_directory()

        print(fs.FileSystem.get_current_work_directory())
        fs.FileSystem.set_path(fs.FileSystem.current_path + "\\" + 'Temporary File')
        print(fs.FileSystem.get_current_work_directory())

        fs.FileSystem.new_file()
        fs.FileSystem.new_directory()

        self.print_message(self.__class__.console_message)
        # self.thread = threading.Thread(target=self.communication.start_server)
        # self.thread.start()

    # attempt to close the server
    def close_server(self):
        print('--Closing Server')
        self.button_stop.place_forget()
        self.button_start.place(x=468, y=0)
        self.print_message("Server is Off!")

        # self.communication.close_server()

    # terminate application execution
    def exit_application(self):
        print('--Exiting Application')
        # self.communication.close_server()
        self.window.destroy()

    # clears the screen with a button
    def clear_screen(self):
        print('--Clearing Screen')
        self.text_box.config(state=NORMAL)
        self.text_box.delete(1.0, "end")
        self.text_box.config(state=DISABLED)

    # print messages to the text box
    # prevents user from typing random stuff in the box
    def print_message(self, message):
        self.text_box.config(state=NORMAL)
        self.text_box.insert(END, ">> " + message + "\n")  # 1.0 insereaza la inceput / END insereaza la sfarsit
        self.text_box.config(state=DISABLED)

    @classmethod
    def console(cls, message):
        cls.console_message = message

    # open the application when running main
    def open_application(self):
        self.__class__.console_message = ''

        # set window attributes
        self.window.geometry("600x400")
        self.window.resizable(0, 0)
        self.window.title('FS Browser - Server')

        # position widgets
        self.button_start.place(x=468, y=0)
        self.button_clear.place(x=468, y=133)
        self.button_exit.place(x=468, y=266)
        self.text_box.place(x=0, y=0)

        # friendly message helper
        self.print_message("Welcome to the Server Interface!\n"
                           ">> To browse the File System, use the Client and type os commands like 'cwd'!")

        # loop the application
        self.window.mainloop()
