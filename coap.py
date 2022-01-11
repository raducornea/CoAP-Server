class CoAP:
    COAP_PAYLOAD_MARKER = 0xff
    COAP_VERSION = 1

    # Message types
    TYPE_CONF = 0
    TYPE_NON_CONF = 1
    TYPE_ACK = 2
    TYPE_RESET = 3

    # Message classes
    CLASS_METHOD = 0
    CLASS_SUCCESS = 2
    CLASS_CLIENT_ERROR = 4
    CLASS_SERVER_ERROR = 5

    # Method codes
    CODE_EMPTY = 0
    CODE_GET = 1
    CODE_POST = 2
    CODE_RENAME = 8
