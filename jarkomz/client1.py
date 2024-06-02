import http.client

IP = input("Enter IP server: ")
Port = input("Enter Port server: ")
connection = http.client.HTTPConnection(IP, Port)

path = input("Enter path or leave blank to quit : ")

while path != ' ' :
    connection.request("GET", path)

    response = connection.getresponse()

    print("Response: ", response.status, response.reason)
    print(response.headers)

    print(response.read().decode())

connconnection.close()
print("Connection to server closed")
