import socket
import threading
import random


localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024
global s, started


# Socket IPv4, UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Asociere la adresa locala, portul 5000
s.bind((localIP, localPort))


def comm_thread(conn, addr):
    while 1:
        # Asteapta date, buffer de 1024 octeti (apel blocant)
        data = conn.recv(1024)

        # Daca functia recv returneaza None, clientul a inchis conexiunea
        if not data: break
        print(addr, ' a trimis: ', data)

        # Trimite inapoi datele receptionate
        conn.sendall(bytes(str(addr) + ' a trimis ' + str(data), encoding="ascii"))

    print("Clientul ", addr, " a inchis conexiunea")
    conn.close()


def close_server():
    global started
    started = False
    print('Server Closed')


def start_server():
    global started
    started = True
    print('Server Started')


def communicate():
    while started:
        rand = random.randint(0, 10)
        message, address = s.recvfrom(1024)

        if rand >= 4:
            s.sendto(message, address)


