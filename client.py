import socket
import time


import threading
import socket
import sys
import select


def receive_fct(s):
    global running
    contor = 0
    while running:
        # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
        # Stabilim un timeout de 1 secunda
        r, _, _ = select.select([s], [], [], 1)
        if not r:
            contor = contor + 1
        else:
            data, address = s.recvfrom(1024)
            print("S-a receptionat ", str(data), " de la ", address)
            print("Contor= ", contor)


def main():
    # communication = server_communication.Communication()
    # communication.start_server()

    # gui = server_gui.GUI()
    # gui.open_application()

    global running

    sport = 2554  # my port
    dport = 2555  # peer port
    dip = "127.0.0.1"  # peer ip

    # Creare socket UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.bind((dip, int(sport)))

    running = True
    try:
        receive_thread = threading.Thread(target=receive_fct, args=(s,))
        receive_thread.start()
    except:
        print("Eroare la pornirea thread‐ului")
        sys.exit()

    while True:
        try:
            data = input("Trimite: ")
            s.sendto(bytes(data, encoding="ascii"), (dip, int(dport)))
        except KeyboardInterrupt:
            running = False
            print("Waiting for the thread to close...")
            receive_thread.join()
            break


if __name__ == '__main__':
    main()
