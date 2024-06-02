import socket
import threading
import os

# Server address and port
address = ("127.0.0.1", 5554)

# Create a TCP/IP socket
sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockets.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sockets.bind(address)
sockets.listen(1)

def read_file(path):
    """Read the content of the file at the given path."""
    with open(path, "r") as file:
        return file.read()

def normalize_path(path):
    """Normalize the requested path to serve the correct file."""
    path = f".{path}"

    if path.endswith("/"):
        path = path[:-1]

    if os.path.isdir(path):
        path += "/index.html"

    return path

def handle_client(csock):
    """Handle the client connection."""
    try:
        msg = csock.recv(4096).decode()
        if not msg:
            return

        head = msg.rstrip().split("\n")[0].split()
        if len(head) < 2:
            return

        path = normalize_path(head[1])

        if not os.path.exists(path):
            csock.send("HTTP/1.1 404 Not Found\r\n".encode())
        else:
            content = read_file(path)
            csock.send(f"HTTP/1.1 200 OK\r\n\r\n{content}\r\n".encode())
    finally:
        csock.close()

def serve():
    """Main server loop to accept connections and start new threads."""
    print(f'Serving on http://{address[0]}:{address[1]}')
    while True:
        csock, client_address = sockets.accept()
        thread = threading.Thread(target=handle_client, args=(csock,))
        thread.start()

if __name__ == '__main__':
    serve()
