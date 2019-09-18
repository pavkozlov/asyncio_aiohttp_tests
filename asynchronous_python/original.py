import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # inet - IPv4, stream - TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # SOL - socket level
                                                                    # (опция относится к уровню сокета)
server_socket.bind(('localhost', 5000))
server_socket.listen()

while True:
    print('Before .accept()')
    client_socket, addr = server_socket.accept()
    print(f'Connections from {addr}')

    while True:
        request = client_socket.recv(4096)
        if not request:
            break
        else:
            response = 'Hello World\n'.encode()
            client_socket.send(response)
    print('outside inner while loop')
    client_socket.close()
