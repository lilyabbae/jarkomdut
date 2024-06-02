import socket
import os

# Alamat server dan port
server_address = ("127.0.0.1", 5554)

# Membuat socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(1)

def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def normalize_path(requested_path):
    normalized_path = f".{requested_path}"  # Menambahkan titik di depan path untuk merujuk ke direktori saat ini

    if normalized_path.endswith("/"):
        normalized_path = normalized_path[:-1]  # Menghapus karakter slash terakhir jika ada

    if os.path.isdir(normalized_path):
        normalized_path += "/index.html"  # Menambahkan index.html jika path adalah direktori

    return normalized_path

def handle_client(client_socket):
    try:
        request = client_socket.recv(4096).decode()  # Menerima pesan dari klien
        if not request:
            return

        # Memisahkan request untuk mendapatkan path yang diminta
        request_line = request.rstrip().split("\n")[0].split()
        if len(request_line) < 2:
            return

        requested_path = normalize_path(request_line[1])

        if not os.path.exists(requested_path):
            client_socket.send("HTTP/1.1 404 Not Found\r\n".encode())  # Mengirim respons 404 jika file tidak ditemukan
        else:
            content = read_file(requested_path)  # Membaca isi file
            response = f"HTTP/1.1 200 OK\r\n\r\n{content}\r\n"
            client_socket.send(response.encode())  # Mengirim respons 200 dengan isi file
    finally:
        client_socket.close()  # Menutup koneksi klien

def start_server():
    print(f'Server berjalan di http://{server_address[0]}:{server_address[1]}')
    while True:
        client_socket, client_address = server_socket.accept()  # Menerima koneksi dari klien
        handle_client(client_socket)  # Menangani klien satu per satu

if __name__ == '__main__':
    start_server()  # Menjalankan server
