import socket, threading
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
port = 10000
sock.bind((host, port))
sock.listen(2)
connections = []


def connect_clients():

    while True:
        c, addr = sock.accept()
        connections.append(c)
        cli_thread = threading.Thread(target=recv_pos, args=[c])
        cli_thread.start()
        cli_thread.getName()


def recv_pos(c):
    while True:
        pos = c.recv(1024)
        if pos:
            send_pos(c, pos)


def send_pos(cli_sock, position):
    for players in connections:
        if players != cli_sock:
            players.send(position)


connect_thread = threading.Thread(target=connect_clients)
connect_thread.start()
