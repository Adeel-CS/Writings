import socket
import threading

HOST = socket.gethostbyaddr(socket.gethostname())
PORT = 55555
BUFFER_SIZE = 1024

# Dictionary to store connected clients and their information
clients = {}

def handle_client(client_socket, client_address):
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE).decode()
            if not data:
                break
            if data.startswith("CALL:"):
                _, sender_username, receiver_username = data.split(":")
                if receiver_username in clients:
                    receiver_socket = clients[receiver_username]['socket']
                    receiver_socket.send(f"INCOMING_CALL:{sender_username}".encode())
                else:
                    client_socket.send(f"ERROR:User {receiver_username} not available.".encode())
            elif data.startswith("CALL_ACCEPTED:"):
                _, receiver_username, sender_username = data.split(":")
                if sender_username in clients:
                    sender_socket = clients[sender_username]['socket']
                    sender_socket.send(f"CALL_ACCEPTED:{receiver_username}".encode())
            elif data.startswith("CALL_DECLINED:"):
                _, receiver_username, sender_username = data.split(":")
                if sender_username in clients:
                    sender_socket = clients[sender_username]['socket']
                    sender_socket.send(f"CALL_DECLINED:{receiver_username}".encode())
            else:
                print(f"Unknown command from client {client_address}: {data}")
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        print(f"[*] Connection established from {client_address}")
        username = client_socket.recv(BUFFER_SIZE).decode()
        clients[username] = {'socket': client_socket, 'address': client_address}
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

    server.close()

if __name__ == "__main__":
    main()
