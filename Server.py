import socket

PORT_NUMBER_USED = 12322
SERVER_NAME = 'localhost'
SERVER_ADDRESS = (SERVER_NAME, PORT_NUMBER_USED)

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(1)

    while True:
        print("Waiting For Connection")
        connection, client_address = server_socket.accept()
        print("Connection From", client_address)
        data = connection.recv(1024).decode()
        print("received: ", data)
        if data:
            print("echoing...")
            connection.sendall(data.encode())
        else:
            print("no more")
        connection.close()