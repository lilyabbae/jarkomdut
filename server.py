import socket
import threading
import os

# Alamat server dan port
address = ("127.0.0.1", 5554)

# Membuat socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(address)
server_socket.listen(1)

def read_file(path):
    """
    Membaca isi file pada path yang diberikan.
    
    Parameter:
    path (str): Lokasi file yang akan dibaca.
    
    Returns:
    str: Isi dari file.
    """
    with open(path, "r") as file:
        return file.read()

def normalize_path(path):
    """
    Menormalkan path yang diminta untuk melayani file yang benar.
    
    Parameter:
    path (str): Path yang diminta oleh klien.
    
    Returns:
    str: Path yang telah dinormalisasi.
    """
    path = f".{path}"  # Menambahkan titik di depan path untuk merujuk ke direktori saat ini

    if path.endswith("/"):
        path = path[:-1]  # Menghapus karakter slash terakhir jika ada

    if os.path.isdir(path):
        path += "/index.html"  # Menambahkan index.html jika path adalah direktori

    return path

def handle_client(client_socket):
    """
    Menangani koneksi dari klien.
    
    Parameter:
    client_socket (socket): Socket klien yang terhubung.
    """
    try:
        request = client_socket.recv(4096).decode()  # Menerima pesan dari klien
        if not request:
            return

        # Memisahkan request untuk mendapatkan path yang diminta
        request_line = request.rstrip().split("\n")[0].split()
        if len(request_line) < 2:
            return

        path = normalize_path(request_line[1])

        if not os.path.exists(path):
            client_socket.send("HTTP/1.1 404 Not Found\r\n".encode())  # Mengirim respons 404 jika file tidak ditemukan
        else:
            content = read_file(path)  # Membaca isi file
            client_socket.send(f"HTTP/1.1 200 OK\r\n\r\n{content}\r\n".encode())  # Mengirim respons 200 dengan isi file
    finally:
        client_socket.close()  # Menutup koneksi klien

def serve():
    """
    Loop utama server untuk menerima koneksi dan memulai thread baru.
    """
    print(f'Serving on http://{address[0]}:{address[1]}')
    while True:
        client_socket, client_address = server_socket.accept()  # Menerima koneksi dari klien
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()  # Memulai thread baru untuk menangani klien

if __name__ == '__main__':
    serve()  # Menjalankan server
