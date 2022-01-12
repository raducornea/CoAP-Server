import json
import threading
import socket
import sys
import select
import message


# the function that interprets the Header & Payload received by the server

def receive_fct(s):
    global running
    counter = 0
    while running:
        r, _, _ = select.select([s], [], [], 1)
        if not r:
            counter = counter + 1
        else:
            data, address = s.recvfrom(1024)
            print("Received", str(data), "from", address)
            # process_data(data, address)
            print("Counter = ", counter)
            client_received_message = message.Message('Server')

            # data is of type packed_data
            header_format, encoded_json = client_received_message.get_header_message(data)

            # decode message so that it can be understood in decimal
            client_received_message.decode_message(header_format, encoded_json)

            # verify header format from data and do CoAP Codes
            encoded_json = client_received_message.get_payload()
            command = json.loads(encoded_json)['command']
            response = json.loads(encoded_json)['response']
            print('COMMAND = ', command)
            print('RESPONSE = ', response)


def main():
    my_message = message.Message('Client')
    global running

    server_port = 2001
    server_ip = "127.0.0.1"

    # make sure every client is connected
    client_port = 2000
    client_ip = "127.0.0.3"

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
            command = input("Command: ")  # 'cwd', 'ls', 'rename'
            parameters = input("Parameters: ")  # old_name new_name
            message_type = int(input("Message Type # 0 conf 1 non-conf 2 ack 3 reset = "))  # int

            """
            GET - cwd, ls -> 0.01 -> GET-> response should be 2.05 (Content)
            The GET method requests a representation of the specified resource. Requests using GET should only 
            retrieve data.

            POST -> 0.02 - newDir, newFile -> response 2.01 (Created)
            The POST method submits an entity to the specified resource, often causing a change in state or side effects 
            on the server.

            PUT -> 0.03 - (move) file and directories? -> 2.04 (Changed)
            The PUT method replaces all current representations of the target resource with the request payload.

            RENAME -> 0.08 - rename -> 2.04 (Changed) Response 
            Renames file/directory
            
            2.00
            This class of Response Code indicates that the clients request was
            successfully received, understood, and accepted.
            
            4.04 Not Found ??? -> Client
            This Response Code is like HTTP 404 "Not Found".
            
            # 408 Request Timeout response - Server Shutdown
            # 499 Client Closed Request - Client Shutdown

            5.01 Not Implemented -> Server
            This Response Code is like HTTP 501 "Not Implemented".
            
            | 2.01 | Created                   
            | 2.04 | Changed                   
            | 2.05 | Content      

            | 4.00 | Bad Request
            | 4.05 | Method Not Allowed - for commands not in the list
            | 4.06 | Not Acceptable - probably for payload marker not respected
            
            | 5.00 | Internal Server Error      
            | 5.01 | Not Implemented            
            
            # client asks for Request (Type 0/1) - does not care for code messages at Request
            # server gives Response (Type 2/3) - cares for code messages
            # client receives Response and interprets it
            """
            my_message.set_msg_version(1)
            my_message.set_msg_token_length(1)
            my_message.set_msg_id(0xffff)
            my_message.set_token(0)
            my_message.set_payload_marker(0xff)

            if command in ['cwd', 'ls']:
                my_message.set_msg_class(0)
                my_message.set_msg_code(1)
            elif command in ['newDir', 'newFile']:
                my_message.set_msg_class(0)
                my_message.set_msg_code(2)
            elif command == ['move']:
                my_message.set_msg_class(0)
                my_message.set_msg_code(3)
            elif command == ['rename']:
                my_message.set_msg_class(0)
                my_message.set_msg_code(8)

            if message_type in [0, 1]:
                my_message.set_msg_type(message_type)
            else:
                my_message.set_msg_type(1)  # non confirmable

            my_message.set_client_payload(command, parameters)
            packed_data = my_message.encode_message()
            s.sendto(packed_data, (server_ip, int(server_port)))

        except KeyboardInterrupt:
            running = False
            print("Waiting for the thread to close...")
            receive_thread.join()
            break


if __name__ == '__main__':
    main()