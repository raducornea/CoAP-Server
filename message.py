import struct
from struct import *
import array

from file_system import send_message_to_listeners


def unpack_helper(fmt, data):
    size = struct.calcsize(fmt)
    return struct.unpack(fmt, data[:size]), data[size:]


class Message:
    def __init__(self):
        # 1 byte: VER + Type + Token Length
        self.msg_version = 1  # 2 bits
        self.msg_type = 1  # 2 bits
        self.msg_token_length = 1  # 4 bits

        # 1 byte: Request/Response Code (Class)(Code)
        self.msg_class = 1  # 0 1 2 - 3 bits
        self.msg_code = 6  # 3 4 5 6 7 - 5 bits

        # 2 bytes: Message ID
        self.msg_id = 0xFffF  # 16 bits

        # 0 - 8 bytes: Token
        self.token = 0

        # 1 byte of 1111 1111
        # 0 - 3 bytes: Payload (if available) -> The message
        self.payload = 'asdf gkj'

    def decode_message(self, message):
        message, my_string = unpack_helper('i i i i i ', message)

        print(message)
        print(my_string)

        msg_version = (0xC0 & message[0]) >> 6
        msg_type = (0x30 & message[0]) >> 4
        msg_token_length = (0x0F & message[0]) >> 0

        msg_class = (message[1] >> 5) & 0b111
        msg_code = (message[1] >> 0) & 0x1F

        msg_id = (message[2] << 8) | message[3]

        self.err_msg_ver(msg_version)
        self.err_msg_tok(msg_token_length)

        token = 0
        if msg_token_length:
            token = message[4]

        my_string = my_string.replace(b'\x00', b'')
        payload = my_string.decode("utf-8")

        print(msg_version)
        print(msg_type)
        print(msg_token_length)
        print(msg_class)
        print(msg_code)
        print(msg_id)
        print(token)
        print(payload)

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
        # todo
        #  de considerat cazul in care sunt mai multi biti decat e voie (FFFF e maximul pt msg_id)
        # daca ai 1024 -> primul are 4, al doilea 0
        message.append(self.msg_id >> 8)

        # daca ai 255 -> primul are 0, al doilea 255
        message.append(self.msg_id & 0xFF)

        """ urmatorii 0-8 octeti """
        message.append(0xFFFFFFFFFFFFFFFF & self.token)

        """ urmatorii 0-4 octeti """
        message.append(self.payload)

        # prepare message to get packed
        packed_data = pack('i i i i i 11s',
                           message[0], message[1], message[2], message[3], message[4], message[5].encode())

        return packed_data

    def err_msg_tok(self, msg_token_length):
        if 9 <= msg_token_length <= 15:
            message = "Eroare la token"
            send_message_to_listeners(message)
            print(message)

    def err_msg_ver(self, msg_version):
        if msg_version != 1:
            message = "Eroare la version"
            send_message_to_listeners(message)
            print(message)

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
