import socket
from select import select

tasks = []
to_read = {}
to_write = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        yield ('read', server_socket)
        client_socket, addr = server_socket.accept()  # read
        print(f'Connections from {addr}')
        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        yield ('read', client_socket)
        request = client_socket.recv(4096)  # read
        if not request:
            break
        else:
            response = 'Hello World\n'.encode()
            yield ('write', client_socket)
            client_socket.send(response)  # write

    client_socket.close()


def event_loop():
    while any([tasks, to_read, to_write]):
        while not tasks:

            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for socks in ready_to_read:
                tasks.append(to_read.pop(socks))

            for socks in ready_to_write:
                tasks.append(to_write.pop(socks))

        try:
            task = tasks.pop(0)
            reason, socks = next(task)

            if reason == 'read':
                to_read[socks] = task
            if reason == 'write':
                to_write[socks] = task
        except StopIteration:
            print('Done!')


tasks.append(server())
event_loop()
