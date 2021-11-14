import server_gui


def main():
    # communication = server_communication.Communication()
    # communication.start_server()

    gui = server_gui.GUI()
    gui.open_application()


if __name__ == '__main__':
    main()


"""
Sources:
https://pythontic.com/modules/socket/udp-client-server-example
https://docs.python.org/3/library/tkinter.html
https://docs.python.org/3/library/socket.html
https://www.geeksforgeeks.org/how-to-use-thread-in-tkinter-python/
https://github.com/nicolaebotezatu/RC-P/blob/main/Non-blocking%20UDP%20peers/udp_peer.py
"""