import http.client
import sys

def main():
    # Pesan penggunaan yang jelas
    usage_message = "Usage: client.py <server_host> <server_port> <filename>"
    if len(sys.argv) != 4:
        print(usage_message)
        return

    # Mendapatkan argumen dari baris perintah
    server_host = sys.argv[1]
    server_port = sys.argv[2]
    filename = sys.argv[3]

    # Informasi tentang request yang akan dibuat
    print(f"Connecting to server at {server_host}:{server_port} to retrieve {filename}")

    try:
        # Membuat koneksi HTTP ke server
        connection = http.client.HTTPConnection(server_host, server_port)
        connection.request("GET", filename)

        # Mendapatkan respons dari server
        response = connection.getresponse()

        # Mencetak status respons
        print(f"Response Status: {response.status} {response.reason}")
        print(f"Headers:\n{response.headers}")

        # Membaca dan mencetak isi dari respons
        content = response.read().decode()
        print("Response Content:\n", content)
        
    except http.client.HTTPException as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Error making request: {err}")
    finally:
        # Menutup koneksi
        if 'connection' in locals():
            connection.close()
            print("Connection to server closed")

if _name_ == "_main_":
    main()
