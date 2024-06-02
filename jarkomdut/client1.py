import http.client

def run_client():
    ServerIP =input("masukan IP server:")
    ServerPort=input("masukan Port server:")
    conn = http.client.HTTPConnection(ServerIP, ServerPort)

    while True:
        path = input("Enter path to request from server (or 'quit' to quit): ")
        if path.lower() == 'quit':
            break

        conn.request("GET", path)

        response = conn.getresponse()

        print("Response: ", response.status, response.reason)
        print(response.headers)

        print(response.read().decode())

    conn.close()
    print("Connection to server closed")

if __name__ == "__main__":
    run_client()
