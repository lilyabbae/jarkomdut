import http.client
import sys

def main():
    print("Usage: client.py server_host server_port filename")

    if len(sys.argv) != 4:
        print("Usage: client.py server_host server_port filename")
        return

    IP = sys.argv[1]
    Port = sys.argv[2]
    path = sys.argv[3]

    try:
        connection = http.client.HTTPConnection(IP, Port)
        connection.request("GET", path)
        response = connection.getresponse()

        print("Response:", response.status, response.reason)
        print(response.headers)
        print(response.read().decode())
    except Exception as e:
        print(f"Error making request: {e}")
    finally:
        connection.close()
        print("Connection to server closed")

if __name__ == "__main__":
    main()
