import json
import socket
import threading
import select

import file_system
import message


class Logic:
    # addresses are tuples like: [("127.0.0.2", 2000), ("127.0.0.3", 2000)]
    client_adresses = []

    server_ip = ""  # server ip
    server_port = 0  # server port
    server_socket = None
    server_received_message = None
    server_response_message = None
    server_client = None  # targeted client in case it disconnects

    data = None
    running = False
    receive_thread = None

    @classmethod
    def __init__(cls):
        # server ip address & port
        cls.server_ip = "127.0.0.1"
        cls.server_port = 2001
        cls.data = None

        cls.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        cls.server_socket.bind((cls.server_ip, cls.server_port))
        cls.server_received_message = message.Message('Client')
        cls.server_response_message = message.Message('Server')
        cls.server_client = None

        # clients addresses # 172.20.10.4 e.g.
        cls.client_adresses = []

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

        # but make sure the message respects CoAP format (Header + Payload as JSON)
        while True:
            if cls.data is not None:
                cls.message_clients(cls.data)

            if not cls.running:  # 408 Request Timeout response - Server Shutdown
                print("TTT Waiting for the thread to close...")

                response = message.Message('Server')
                response.set_msg_version(1)
                response.set_msg_token_length(1)
                response.set_msg_id(0xffff)
                response.set_token(0)
                response.set_payload_marker(0xff)

                response.set_msg_class(4)
                response.set_msg_code(0)
                response.set_msg_type(8)
                response.set_payload_marker(0xff)
                response.set_payload("Server has Quit!")

                cls.message_clients(response)

                cls.receive_thread.join()
                print("TTT Thread receive_thread closed")
                break

    @classmethod
    def message_clients(cls, message_to_send):
        # send clients the message
        # only when cls.data != None will it send to listeners
        for i in range(len(cls.client_adresses)):
            ip = cls.client_adresses[i][0]
            port = cls.client_adresses[i][1]
            cls.server_socket.sendto(message_to_send, (ip, port))
        cls.data = None

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
                # server connects to clients as well when they send a message
                data, address = cls.server_socket.recvfrom(1024)
                print("Received", str(data), "from", address)

                # add client address when client sends to server
                if address not in cls.client_adresses:
                    cls.client_adresses.append(address)

                # process data
                cls.process_data(data, address)
                print("Counter = ", counter)

    @classmethod
    def process_data(cls, data, address):
        cls.server_client = address

        # data is of type packed_data
        header_format, encoded_json = cls.server_received_message.get_header_message(data)

        # decode message so that it can be understood in decimal
        cls.server_received_message.decode_message(header_format, encoded_json)

        # verify header format from data and do CoAP Codes
        cls.server_response_message = cls.server_received_message.verify_format()
        cls.data = cls.server_response_message.encode_message()

    @classmethod
    def disconnect_client(cls):  # 499 Client Closed Request
        # disconnecting targeted client
        cls.client_adresses.remove(cls.server_client)

        response = message.Message('Server')
        response.set_msg_version(1)
        response.set_msg_token_length(1)
        response.set_msg_id(0xffff)
        response.set_token(0)
        response.set_payload_marker(0xff)

        response.set_msg_class(4)
        response.set_msg_code(9)
        response.set_msg_type(9)
        response.set_payload_marker(0xff)
        response.set_payload("Adress " + cls.server_client + " Disconnected!")

        cls.message_clients(response)
        cls.server_client = None
