import cv2
import socket
import pickle
import struct

HOST = socket.gethostbyaddr(socket.gethostname())
PORT = 55555

def video_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Connection established from {addr}")

        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            data = pickle.dumps(frame)
            message_size = struct.pack("L", len(data))
            client_socket.sendall(message_size + data)

            cv2.imshow('Server', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        client_socket.close()

def main():
    video_server()

if __name__ == "__main__":
    main()
