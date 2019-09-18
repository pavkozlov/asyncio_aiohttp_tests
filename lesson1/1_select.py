import socket
from select import select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()

to_monitor = []


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print(f'Connections from {addr}')
    to_monitor.append(client_socket)


def send_message(client_socket):
    request = client_socket.recv(4096)
    if request:
        response = 'Hello World\n'.encode()
        client_socket.send(response)
    else:
        to_monitor.remove(client_socket)
        client_socket.close()


def event_loop():
    while True:
        ready_to_read, _, _ = select(to_monitor, [], [])  # ready_to_write, exceptions
        for socks in ready_to_read:
            if socks is server_socket:
                accept_connection(socks)
            else:
                send_message(socks)


if __name__ == '__main__':
    to_monitor.append(server_socket)
    event_loop()
