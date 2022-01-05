import threading
import socket
import sys
import select


def receive_fct(s):
    global running
    contor = 0
    while running:
        r, _, _ = select.select([s], [], [], 1)
        if not r:
            contor = contor + 1
        else:
            data, address = s.recvfrom(1024)
            print("S-a receptionat ", str(data), " de la ", address)
            print("Contor= ", contor)


def main():
    global running

    server_port = 2001
    server_ip = "127.0.0.1"

    # make sure every client is connected
    client_port = 2000
    client_ip = "127.0.0.2"

    # Creare socket UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.bind((client_ip, int(client_port)))

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
            s.sendto(bytes(data, encoding="ascii"), (server_ip, int(server_port)))
        except KeyboardInterrupt:
            running = False
            print("Waiting for the thread to close...")
            receive_thread.join()
            break


if __name__ == '__main__':
    main()