import socket
import threading
import select


class Logic:
    server_socket = None
    ip = ""  # ip for client and server
    server_port = 0  # server port
    client_port = 0  # client port
    data = None
    running = False
    receive_thread = None

    # TODO
    #  - make ip addresses into a list of connected [connected ips]
    #  - each time a client connects => add it into [connected ips] + remove from list when [disconnected]

    @classmethod
    def __init__(cls):
        cls.ip = "127.0.0.1"  # local ip both client and server have  # ip-ul clientului  172.20.10.4
        cls.server_port = 2001  # my port
        cls.client_port = 2000  # peer port
        cls.data = None

        cls.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        cls.server_socket.bind(("127.0.0.2", cls.server_port))  # asta ar trebui scoasa -> de abia cand primeste mesaj
        # realizeaza conexiunea cu ip-ul pe care il primeste

        cls.running = False
        cls.receive_thread = threading.Thread(target=cls.receive_fct, args=(cls.server_socket,))

    @classmethod
    def server_start(cls):
        cls.running = True
        cls.send_to_client()

    @classmethod
    def server_stop(cls):
        cls.running = False

    @classmethod
    def set_data(cls, data):
        cls.data = data

    @classmethod
    def send_to_client(cls):
        try:
            cls.receive_thread = threading.Thread(target=cls.receive_fct)
            cls.receive_thread.start()
        except:
            print("TTT Error at starting Thread")
            return

        while True:
            data = cls.data
            if data is not None:
                # data ar trebui sa fie efectiv tot pachetul cu toate campurile inclusiv payload ca json
                cls.server_socket.sendto(bytes(data, encoding="ascii"), (cls.ip, int(cls.client_port)))
                # ar trebui modificat si el, incat sa se adapteze fiecarui ip noi primit din data de la client
                cls.data = None
            if not cls.running:
                print("TTT Waiting for the thread to close...")
                cls.receive_thread.join()
                print("TTT Thread receive_thread closed")
                break

    @classmethod
    def receive_fct(cls):
        counter = 0
        while cls.running:
            # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
            # Stabilim un timeout de 1 secunda
            r, _, _ = select.select([cls.server_socket], [], [], 1)
            if not r:
                counter = counter + 1
            else:
                data, address = cls.server_socket.recvfrom(1024)
                print("Received ", str(data), " from ", address)
                # aici ar trebui sa decodific data, incat sa aflu ip-ul
                print("Counter = ", counter)
