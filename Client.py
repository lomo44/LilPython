import socket

PORT_NUMBER_USED = 12322
SERVER_NAME = 'localhost'
SERVER_ADDRESS = (SERVER_NAME, PORT_NUMBER_USED)

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)
    try:
        message = "This is the message"
        client_socket.sendall(message.encode())
        amount_received = 0
        amount_send = len(message)

        while amount_received < amount_send:
            data = client_socket.recv(1024).decode()
            amount_received += len(data)
            print("received:", data)
    finally:
        client_socket.close()