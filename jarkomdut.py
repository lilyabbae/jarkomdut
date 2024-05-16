import socket
import signal
import sys
import os
import pathlib

def init():
    port = 3000
    address = ("127.0.0.1", port)
    sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockets.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sockets.bind(address)
    sockets.listen(1)
    return {"socket": sockets, "address": address}

def read_file(path):
    line = ""
    with open(path, "r") as file:
        line = file.read()
    return line

def normalize_path(path):
    path = f".{path}"

    if path.endswith("/"):
        path = path[:-1]

    if os.path.isdir(path):
        path += "/index.html"
    
    return path

def serve(http, callback=lambda host, port: None):
    def sigint_handler(sig, frame):
        close(http)
        sys.exit(0)

    signal.signal(signal.SIGINT, sigint_handler)
    callback(http["address"][0], http["address"][1])

    while True:
        (csock, address) = http["socket"].accept()
        msg = csock.recv(4096).decode()

        head = msg.rstrip().split("\n")[0].split()
        path = normalize_path(head[1])

        if not os.path.exists(path):
            csock.send(f"HTTP/1.1 404 Not Found\r\n".encode())
            csock.close()
            continue

        content = read_file(path)
        csock.send(f"HTTP/1.1 200 OK\n\n{content}\r\n".encode())
        csock.close()

def close(http):
    http["socket"].close()

server = init()
serve(server, lambda host, port: print(f"Listening on http://{host}:{port}"))