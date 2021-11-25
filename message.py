import struct


class Message:
    def __init__(self):
        # 1 byte: VER + Type + Token Length
        self.msg_version = 0  # 2 bits
        self.msg_type = 0  # 2 bits
        self.msg_token_length = 0  # 4 bits

        # 1 byte: Request/Response Code (Class)(Code)
        self.msg_class = 0  # 0 1 2 - 3 bits
        self.msg_code = 0  # 3 4 5 6 7 - 5 bits

        # 2 bytes: Message ID
        self.msg_id = 0  # 16 bits

        # 0 - 8 bytes: Token
        self.token = 0

        # 0 - 4 bytes: Options (if available)
        self.options = []

        # 1 byte of 1111 1111
        # 0 - 3 bytes: Payload (if available) -> The message
        self.payload = ''

    """
    def get_message(self, msg_version, msg_type, msg_token_length, msg_class, msg_code, msg_id, token, options, payload):
    self.msg_version = format(msg_version, '02b')
        self.msg_type = format(msg_type, '02b')
        self.msg_token_length = format(msg_token_length, '04b')
        self.msg_class = format(msg_class, '03b')
        self.msg_code = format(msg_code, '05b')
        self.msg_id = format(msg_id, '016b')
        self.token = format(token, '064b')
        self.options = format(options, '032b')
        self.payload = format(payload, '024b')
    """
    def get_message(self, message):
        """
        message: full message header with everything in it
        """
        received_message = struct.unpack('hhl', message)
        self.msg_version = received_message[0]
        self.msg_type = received_message[1]
        self.msg_token_length = received_message[2]
        self.msg_class = received_message[3]
        self.msg_code = received_message[4]
        self.msg_id = received_message[5]
        self.token = received_message[6]
        self.options = received_message[7]
        self.payload = received_message[8]

    def send_message(self):
        message_to_send = struct.pack('hhl', self.msg_version, self.msg_type, self.msg_token_length, self.msg_class,
                                      self.msg_code, self.msg_id, self.token, self.options, self.payload)
        return message_to_send

    @classmethod
    def decode_message(cls, message: bytes):
        msg_version = (0xC0 & message[0]) >> 6
        msg_type = (0x30 & message[0]) >> 4
        msg_token_length = (0x0F & message[0]) >> 0
        msg_class = (message[1] >> 5) & 0b111
        msg_code = (message[1] >> 0) & 0x1F
        msg_id = (message[2] << 8) | message[3]

        if msg_version != 1:
            print("Error")

        if 9 <= msg_token_length <= 15:
            print("Error")

        token = 0
        if msg_token_length:
            token = message[4:4 + msg_token_length]

        payload = message[5 + msg_token_length:].decode('utf-8')
        return cls(payload, msg_type, msg_class, msg_code, msg_id, msg_token_length, msg_version=1, token=0)

    def encode_message(self):
        message = [(0x03 & self.msg_version) << 6]

        message[0] |= ((self.msg_type & 0b11) << 4)
        message[0] |= (self.msg_token_length & 0x0F)

        message.append((self.msg_class & 0b11) << 5)
        message[1] |= (self.msg_code & 0x1F)

        message.append(self.msg_id >> 8)
        message.append(self.msg_id & 0xFF)

        if self.msg_token_length:
            message = (message << 8 * self.msg_token_length) | self.token

        if len(self.payload):
            self.payload.encode('utf-8')
        for i in range(0, len(self.payload)):
            message.append(self.payload[i])

        return message.to_bytes(message + self.msg_token_length, 'big')