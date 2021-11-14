import socket
import time


UDP_IP = "127.0.0.1"
UDP_PORT = 5000


def main():
    for pings in range(10):
        # Creaza un socket IPv4, UDP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.settimeout(1)

        message = b'test'
        addr = (UDP_IP, UDP_PORT)

        start = time.time()

        s.sendto(message, addr)
        try:
            data, server = s.recvfrom(1024)
            end = time.time()
            elapsed = end - start
            print(data)
        except socket.timeout:
            print('Request timed out')


if __name__ == '__main__':
    main()
