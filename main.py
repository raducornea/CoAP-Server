import server_gui
import file_system as fs


def main():
    FS = fs.FileSystem()
    FS.get_current_work_directory()

    FS.new_file()
    FS.new_directory()

    print(FS.get_current_work_directory())
    FS.set_path(FS.current_path + "\\" + 'Temporary File')
    print(FS.get_current_work_directory())

    FS.new_file()
    FS.new_directory()

    gui = server_gui.GUI()
    gui.open_application()


if __name__ == '__main__':
    main()












"""
Sources:
https://pythontic.com/modules/socket/udp-client-server-example
https://docs.python.org/3/library/tkinter.html
https://docs.python.org/3/library/socket.html
https://docs.python.org/3/library/os.html
https://www.geeksforgeeks.org/how-to-use-thread-in-tkinter-python/
https://github.com/nicolaebotezatu/RC-P/blob/main/Non-blocking%20UDP%20peers/udp_peer.py
https://thispointer.com/how-to-create-a-directory-in-python/

"""