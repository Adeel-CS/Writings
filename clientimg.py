import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 55555

# Function to receive messages from the server
def receive_messages(client_socket):
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

                    # Save and view the received image
                    with open('received_image.jpg', 'wb') as file:
                        file.write(image_data)
                    image = Image.open('received_image.jpg')
                    image.show()
                else:
                    print(message.decode('utf-8'))
        except Exception as e:
            print("Error receiving message:", e)
            break

# Main function to start the client
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Start a separate thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    # Send messages to the server
    while True:
        message = input()
        if message.lower() == 'exit':
            break
        elif message.lower() == 'image':
            # Send image to the server
            client.send(message.encode('utf-8'))
            with open('example_image.jpg', 'rb') as file:
                image_data = file.read()
                client.send(image_data)
        else:
            client.send(message.encode('utf-8'))

    client.close()

if __name__ == "__main__":
    main()
