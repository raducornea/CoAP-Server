import struct
from struct import *
import json

import file_system
import server_gui
import server_logic


def unpack_helper(fmt, data):
    size = struct.calcsize(fmt)
    return struct.unpack(fmt, data[:size]), data[size:]


class Message:
    def __init__(self, architecture_type):
        self.architecture_type = architecture_type  # server / client

        # 1 byte: VER + Type + Token Length
        self.msg_version = 1  # 2 bits  # must always be 1
        self.msg_type = 1  # 2 bits  # 0 conf 1 non-conf 2 ack 3 reset
        self.msg_token_length = 0  # 4 bits  # must be outside [9, 15]

        # GET / PUT / POST / RENAME - given by these codes
        # 1 byte: Request/Response Code (Class)(Code)  # 4.04
        self.msg_class = 2  # 0 1 2 - 3 bits  #  0-7
        self.msg_code = 5  # 3 4 5 6 7 - 5 bits  # 0-31

        # 2 bytes: Message ID
        self.msg_id = 0xFffF  # 16 bits

        # 0 - 8 bytes: Token
        self.token = 0

        # 1 byte of (1111 1111) for payload_marker
        self.payload_marker = 0xff

        # 0 - 3 bytes: Payload (if available) -> The message
        self.payload = {'command': 'cwd'}

    def set_msg_version(self, msg_version):
        self.msg_version = msg_version

    def set_msg_type(self, msg_type):
        self.msg_type = msg_type

    def set_msg_token_length(self, msg_token_length):
        self.msg_token_length = msg_token_length

    def set_msg_class(self, msg_class):
        self.msg_class = msg_class

    def set_msg_code(self, msg_code):
        self.msg_code = msg_code

    def set_msg_id(self, msg_id):
        self.msg_id = msg_id

    def set_token(self, token):
        self.token = token

    def set_payload_marker(self, marker):
        self.payload_marker = marker

    def set_payload(self, payload):
        self.payload = payload

    # function for server only
    def set_server_payload(self, command, response):
        if self.architecture_type == 'Server':
            self.payload = {'command': command, 'response': response}

    # function for client only
    def set_client_payload(self, command, parameters):
        if self.architecture_type == 'Client':
            self.payload = {'command': command, 'parameters': parameters}

    def err_msg_tok(self, msg_token_length):
        # TREBUIE procesate ca eroare de formatare mesaj
        if 9 <= msg_token_length <= 15:
            message = "Eroare la token"
            file_system.send_message_to_listeners(message)
            print(message)
            return False
        return True

    # verify format prepares another message to send depending on its parameters
    def verify_format(self):
        # prepare response for Client (the response is of type server)
        if self.architecture_type == 'Client':
            response = Message('Server')

            response.set_msg_version(1)
            # non-conf
            response.set_msg_type(1)
            response.set_msg_token_length(1)
            response.set_msg_id(0xffff)
            response.set_token(0)
            response.set_payload_marker(0xff)

            # if message received wants acknowledgement (is confirmable)
            if self.msg_type == 0:
                # ack
                response.set_msg_type(2)
                # 2.00 - Success
                response.set_msg_class(2)
                response.set_msg_code(0)
                response.set_msg_type(0)

                # use next line until client can process other information than jsons of type client
                response.set_server_payload('ANY COMMAND', 'ACK from SERVER')
                server_logic.Logic.message_clients(response.encode_message())
                # response.set_payload("Success. Message Received")  # use it only when it's success

                # conf
                response.set_server_payload('ANY COMMAND', 'response from server')
                response.set_msg_type(0)
                print("ajunge aici")
                return response

            if self.msg_version != 1:
                # Unknwon Version MUST be silently ignored
                message = "Client Header Version Error"  # 500 Internal Server Error
                server_gui.GUI.print_message(message)

                response.set_msg_class(4)
                response.set_msg_code(0)
                response.set_msg_type(0)
                response.set_payload_marker(0)
                response.set_payload("")
                return response

            # try to decode the message received by the server from the client
            try:
                encoded_json = self.get_payload()  # b'{"command": "hello", "parameters": "hi"}'
                command = json.loads(encoded_json)['command']
                parameters = json.loads(encoded_json)['parameters']
                print(encoded_json)

            except KeyError:
                print('Invalid Command/Parameters')  # bad gateway 5.02
                response.set_msg_class(5)
                response.set_msg_code(2)
                response.set_msg_type(3)  # reset - received it, ccould not process
                return response

            response.set_server_payload(command, 'A MERS???')

            # remove client address if command is 'disconnected' - should not care about the message format
            if command == 'disconnect':
                # forcefully disconnect client and announce other clients of it's disconnection
                server_logic.Logic.disconnect_client()
                return

            # if both command and parameters are recognized, continue unit tests
            print(command)
            print(parameters)

            return response
        else:
            new_message = Message('Client')

        # check type
        # 1. Cererea (Request)
        # Confirmable (0) - mesajul asteapta mesajul de confirmare
        # Non-Confirmabil (1) - mesaj care nu asteapta mesaj de confirmare
        # 2. Raspuns (Response)
        # Acknowledgement (2) - mesaj de tip raspuns care confirma un mesaj confirmabil (0)
        # Reset (3) - mesaj care indica primirea unui mesaj, dar nu l-a putut procesa

        """
        The absence of the  Payload Marker denotes a zero-length payload.  
        The presence of a
        marker followed by a zero-length payload MUST be processed as a
        message format error.
        """

        print(self.msg_version)
        print(self.msg_type)
        print(self.msg_token_length)
        print(self.msg_class)
        print(self.msg_code)
        print(self.msg_id)
        print(self.token)
        print(self.payload_marker)
        print(self.payload)  # cwd

    # make message understandable in decimal
    def decode_message(self, message, encoded_json):
        self.msg_version = (0xC0 & message[0]) >> 6
        self.msg_type = (0x30 & message[0]) >> 4
        self.msg_token_length = (0x0F & message[0]) >> 0

        self.msg_class = (message[1] >> 5) & 0b111
        self.msg_code = (message[1] >> 0) & 0x1F

        self.msg_id = (message[2] << 8) | message[3]

        self.payload_marker = (message[3])
        self.payload = encoded_json

        self.token = 0
        if self.msg_token_length:
            self.token = message[4]

    # get the header_format and encoded_json from the message from received
    # by client/server
    def get_header_message(self, message):
        header_format, encoded_json = unpack_helper('i i i i i i ', message)
        encoded_json = encoded_json.replace(b'\x00', b'')
        return header_format, encoded_json

    # format the message so that it can respect CoAP formating and put the
    # commands/outputs/parameters in JSON
    def encode_message(self):
        """ primul octet """
        # ((11 & VER) << 6) = 8 biti
        message = [(0x03 & self.msg_version) << 6]

        # ((11 & VER) << 6) + ((11 & type) << 4) -> pui in cei 8 biti noul numar
        message[0] |= ((self.msg_type & 0x03) << 4)

        # 1111 & length -> il aduni cu message si obtii tot un numar pe 8 biti
        message[0] |= (self.msg_token_length & 0x0F)

        """ al doilea octet format din clasa si cod (3 + 5) """
        # ((11 & msg_class) << 5) = 8 biti
        message.append((0x03 & self.msg_class) << 5)

        # aduni (0001 1111 & msg_code) la message[1] si obtii class + code
        message[1] |= (self.msg_code & 0x1F)

        """ urmatorii 2 octeti """
        # daca ai 1024 -> primul are 4, al doilea 0
        message.append(self.msg_id >> 8)

        # daca ai 255 -> primul are 0, al doilea 255
        message.append(self.msg_id & 0xFF)

        """ urmatorii 0-8 octeti """
        message.append(0xFFFFFFFFFFFFFFFF & self.token)

        """ urmatorul 1 octet"""
        message.append(0xFF & self.payload_marker)

        """ urmatorii 0-3 octeti """
        message.append(self.payload)  # message[6]
        json_message = json.dumps(message[6])
        json_size = len(json_message)
        json_message = json_message.encode()

        # prepare message to get packed
        packed_data = pack('i i i i i i ' + str(json_size) + 's',
                           message[0], message[1], message[2], message[3], message[4], message[5], json_message)

        return packed_data

    def get_version(self):
        return int(str(self.msg_version), 2)

    def get_type(self):
        return self.msg_type  # int(str(self.msg_type))

    def get_class(self):
        return int(str(self.msg_class))

    def get_code(self):
        return self.msg_code

    def get_message_id(self):
        return int(str(self.msg_id))

    def get_token(self):
        return int(str(self.token))

    def get_payload(self):
        return self.payload

    def print_details(self):
        print("We are printing the message format...")
        print("VERSION: " + str(self.get_version()))
        print("TYPE: " + str(self.get_type()))
        print("CLASS.CODE: " + (str(self.get_class()) + "." + str(self.get_code())))
        print("MESSAGE ID: " + str(self.get_message_id()))
        print("Token: " + str(self.get_token()))
        print("Payload: " + str(self.get_payload()))
