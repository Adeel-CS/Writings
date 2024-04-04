import socket
import threading
from PIL import Image

# Server configuration
HOST = socket.gethostbyaddr(socket.gethostname())
PORT = 55555

# List to store connected clients
clients = []

# Function to handle client connections
def handle_client(client_socket, client_address):
    # Add the client to the list of connected clients
    clients.append(client_socket)
    print(f"[*] {client_address} connected.")

    # Receive and broadcast messages
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                if message.decode('utf-8') == 'image':
                    # Receive image data
                    image_data = client_socket.recv(1024)
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        image_data += data

                    # Save the received image
                    with open('received_image.jpg', 'wb') as file:
                        file.write(image_data)
                    print(f"Image received from {client_address}")

                    # Broadcast image to all clients
                    broadcast_image(image_data, client_socket)
                else:
                    print(f"Message from {client_address}: {message.decode('utf-8')}")
                    broadcast(message, client_socket)
        except Exception as e:
            print(f"[*] {client_address} disconnected.")
            clients.remove(client_socket)
            client_socket.close()
            break

# Function to broadcast message to all clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except Exception as e:
                print(e)
                client.close()
                clients.remove(client)

# Function to broadcast image to all clients
def broadcast_image(image_data, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(b'image')
                client.send(image_data)
            except Exception as e:
                print(e)
                client.close()
                clients.remove(client)

# Main function to start the server
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    main()
