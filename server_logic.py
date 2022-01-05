import socket
import threading
import select


class Logic:
    client_ips = []  # clients ip
    client_ports = []  # clients port

    server_ip = ""  # server ip
    server_port = 0  # server port
    server_socket = None

    data = None
    running = False
    receive_thread = None

    # TODO
    #  - each time a client connects => add it into [connected ips] + remove from list when [disconnected]

    @classmethod
    def __init__(cls):
        # adresa ip a server-ului
        cls.server_ip = "127.0.0.1"
        cls.server_port = 2001  # my port
        cls.data = None

        cls.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        cls.server_socket.bind((cls.server_ip, cls.server_port))  # asta ar trebui scoasa -> de abia cand primeste mesaj
        # realizeaza conexiunea cu ip-ul pe care il primeste

        # adresele clientilor # ip-ul clientului 172.20.10.4
        cls.client_ips = ["127.0.0.2", "127.0.0.3"]  # clients ips
        cls.client_ports = [2000, 2000]  # clients ports

        cls.running = False
        cls.receive_thread = threading.Thread(target=cls.receive_fct, args=(cls.server_socket,))

    @classmethod
    def server_start(cls):
        cls.running = True
        cls.send_to_clients()

    @classmethod
    def server_stop(cls):
        cls.running = False

    @classmethod
    def set_data(cls, data):
        cls.data = data

    @classmethod
    def send_to_clients(cls):
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

                # trimitem tuturor clientilor acelasi mesaj
                for i in range(len(cls.client_ports)):
                    ip = cls.client_ips[i]
                    port = cls.client_ports[i]
                    cls.server_socket.sendto(bytes(data, encoding="ascii"), (ip, port))

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