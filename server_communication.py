import socket
import sys
import threading
import select


class Communication:
    def __init__(self):
        self.dip = "127.0.0.1"  # local ip both client and server have
        self.sport = 2555  # my port
        self.dport = 2554  # peer port
        self.bufferSize = 1024

        # Creare socket UDP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.running = False
        self.receive_thread = threading.Thread(target=self.receive_fct, args=(self.s,))

    def close_server(self):
        self.running = False
        self.receive_thread.join()
        self.s.close()

    def start_server(self):
        print('Server Started')
        self.__init__()
        self.s.bind(("127.0.0.1", int(self.sport)))
        self.communicate()

    def communicate(self):
        self.running = True
        try:
            self.receive_thread = threading.Thread(target=self.receive_fct, args=(self.s, ))
            self.receive_thread.start()
        except:
            print("Eroare la pornirea thread‐ului")
            sys.exit()

        while True:
            try:
                # TODO: de corectat cand pornesc serverul
                # https://stackoverflow.com/questions/16745507/tkinter-how-to-use-threads-to-preventing-main-event-loop-from-freezing
                # cozi de mesaje???
                data = input("Trimite: ")

                if data is not None:
                    self.s.sendto(bytes(data, encoding="ascii"), (self.dip, int(self.dport)))
            except KeyboardInterrupt:
                self.running = False
                print("Waiting for the thread to close...")
                self.receive_thread.join()
                break

    def receive_fct(self, s):
        contor = 0
        while self.running:
            # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
            # Stabilim un timeout de 1 secunda
            r, _, _ = select.select([s], [], [], 1)
            if not r:
                contor = contor + 1
            else:
                data, address = s.recvfrom(1024)
                print("S-a receptionat ", str(data), " de la ", address)
                print("Contor= ", contor)
