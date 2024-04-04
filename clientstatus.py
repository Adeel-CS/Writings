import socket

HOST = '127.0.0.1'
PORT = 55555
BUFFER_SIZE = 1024

def set_status(username, status):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.send(f"SET_STATUS:{username}:{status}".encode())
        response = client.recv(BUFFER_SIZE).decode()
        print(response)

def get_status(username):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.send(f"GET_STATUS:{username}".encode())
        status = client.recv(BUFFER_SIZE).decode()
        print(f"Status for {username}: {status}")

def main():
    while True:
        print("1. Set Status")
        print("2. Get Status")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            username = input("Enter your username: ")
            status = input("Enter your status: ")
            set_status(username, status)
        elif choice == '2':
            username = input("Enter username to get status: ")
            get_status(username)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
