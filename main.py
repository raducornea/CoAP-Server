import server_gui
import message
from struct import *


def main():
    """
    # Struct - pack & unpack
    from struct import *


    packed_data = pack("13s i", b"hello, bro", 252525242)
    print(packed_data)

    print(calcsize("13si"))
    # i       - 1i (i needs 4 bytes)
    # b b b b - 4s
    # b b b b - 4s
    # b b b b - 4s
    # b x x x - 1s
    # 13s + i -> 20 bytes necessary

    unpacked_date = unpack("13s i", packed_data)
    print(unpacked_date)
    """
    my_message = message.Message()
    my_message.print_details()

    packed_data = my_message.encode_message()
    print(packed_data)
    my_message.decode_message(packed_data)

    gui = server_gui.GUI()
    gui.open_application()


if __name__ == '__main__':
    main()

"""
Sources:
https://www.youtube.com/watch?v=y49OUKBCEek&ab_channel=AshaTutorials
https://www.youtube.com/watch?v=-dErxklW4_4&ab_channel=seanwasereytbe
https://pythontic.com/modules/socket/udp-client-server-example
https://docs.python.org/3/library/tkinter.html
https://docs.python.org/3/library/socket.html
https://docs.python.org/3/library/os.html
https://www.geeksforgeeks.org/how-to-use-thread-in-tkinter-python/
https://github.com/nicolaebotezatu/RC-P/blob/main/Non-blocking%20UDP%20peers/udp_peer.py
https://levelup.gitconnected.com/method-types-in-python-2c95d46281cd
https://www.pythonprogramming.in/how-to-access-both-cls-and-self-in-a-method-in-python.html
https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter
https://thispointer.com/how-to-create-a-directory-in-python/

"""
