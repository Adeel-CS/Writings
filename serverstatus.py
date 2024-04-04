import socket

HOST = socket.gethostbyaddr(socket.gethostname())
PORT = 55555
BUFFER_SIZE = 1024

statuses = {}

def handle_client(conn):
    while True:
        data = conn.recv(BUFFER_SIZE).decode()
        if not data:
            break
        if data.startswith("SET_STATUS:"):
            _, username, status = data.split(":")
            statuses[username] = status
            print(f"Status updated for {username}")
            conn.send("Status updated successfully!".encode())
        elif data.startswith("GET_STATUS:"):
            _, username = data.split(":")
            status = statuses.get(username, "No status set")
            conn.send(status.encode())
        else:
            print(f"Unknown command from client: {data}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[*] Connection established from {addr}")
        handle_client(conn)

    server.close()

if __name__ == "__main__":
    main()
