import socket
import threading

HOST = '127.0.0.1'
PORT = 55555
BUFFER_SIZE = 1024

def receive_data(client_socket):
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE).decode()
            if not data:
                break
            print(data)
        except Exception as e:
            print("Error receiving data:", e)
            break

def main():
    username = input("Enter your username: ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.send(username.encode())
    
    receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
    receive_thread.start()

    while True:
        print("1. Call")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            receiver_username = input("Enter username to call: ")
            client_socket.send(f"CALL:{username}:{receiver_username}".encode())
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please try again.")

    client_socket.close()

if __name__ == "__main__":
    main()
