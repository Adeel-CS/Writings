from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import socket

clients = {}
addresses = {}

HOST = socket.gethostname()
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket.socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave!"+
                          "Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            if msg.startswith(b"@"):  # Private message
                recipient_name, private_msg = msg.decode("utf8")[1:].split(" ", 1)
                send_private_message(name, recipient_name, private_msg)
            else:  # Group message
                broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

def send_private_message(sender_name, recipient_name, msg):
    """Sends a private message to a specific client."""
    recipient_found = False
    for sock, name in clients.items():
        if name == recipient_name:
            recipient_found = True
            recipient_socket = sock
            break
    if recipient_found:
        recipient_socket.send(bytes("[Private from %s] %s" % (sender_name, msg), "utf8"))
    else:
        sender_socket = [sock for sock, name in clients.items() if name == sender_name][0]
        sender_socket.send(bytes("Recipient '%s' not found." % recipient_name, "utf8"))

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()














# from socket import AF_INET, socket, SOCK_STREAM
# from threading import Thread
# import socket
# clients = {}
# addresses = {}
# HOST = socket.gethostbyaddr(socket.gethostname())
# PORT = 33000
# BUFSIZ = 1024
# ADDR = (HOST, PORT)
# SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# SERVER.bind((HOST, int(PORT)))


# def accept_incoming_connections():
#     """Sets up handling for incoming clients."""
#     while True:
#         client, client_address = SERVER.accept()
#         print("%s:%s has connected." % client_address)
#         client.send(bytes("Greetings from the cave!"+
#                           "Now type your name and press enter!", "utf8"))
#         addresses[client] = client_address
#         Thread(target=handle_client, args=(client,)).start()
# # def handle_client(client):  # Takes client socket as argument.
# #     """Handles a single client connection."""
# #     name = client.recv(BUFSIZ).decode("utf8")
# #     welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
# #     client.send(bytes(welcome, "utf8"))
# #     msg = "%s has joined the chat!" % name
# #     broadcast(bytes(msg, "utf8"))
# #     clients[client] = name
# #     while True:
# #         msg = client.recv(BUFSIZ)
# #         if msg != bytes("{quit}", "utf8"):
# #             broadcast(msg, name+": ")
# #         else:
# #             client.send(bytes("{quit}", "utf8"))
# #             client.close()
# #             del clients[client]
# #             broadcast(bytes("%s has left the chat." % name, "utf8"))
# #             break
# def handle_client(client):
#     """Handles a single client connection."""
#     name = client.recv(BUFSIZ).decode("utf8")
#     welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
#     client.send(bytes(welcome, "utf8"))
#     msg = "%s has joined the chat!" % name
#     broadcast(bytes(msg, "utf8"))
#     clients[client] = name
#     while True:
#         msg = client.recv(BUFSIZ)
#         if msg != bytes("{quit}", "utf8"):
#             if msg.startswith(b"@"):  # Private message
#                 recipient_name, private_msg = msg.decode("utf8")[1:].split(" ", 1)
#                 send_private_message(name, recipient_name, private_msg)
#             else:  # Group message
#                 broadcast(msg, name+": ")
#         else:
#             client.send(bytes("{quit}", "utf8"))
#             client.close()
#             del clients[client]
#             broadcast(bytes("%s has left the chat." % name, "utf8"))
#             break

# def send_private_message(sender_name, recipient_name, msg):
#     """Sends a private message to a specific client."""
#     recipient_found = False
#     for sock, name in clients.items():
#         if name == recipient_name:
#             recipient_found = True
#             recipient_socket = sock
#             break
#     if recipient_found:
#         recipient_socket.send(bytes("[Private from %s] %s" % (sender_name, msg), "utf8"))
#     else:
#         sender_socket = [sock for sock, name in clients.items() if name == sender_name][0]
#         sender_socket.send(bytes("Recipient '%s' not found." % recipient_name, "utf8"))

# def broadcast(msg, prefix=""):  # prefix is for name identification.
#     """Broadcasts a message to all the clients."""
#     for sock in clients:
#         sock.send(bytes(prefix, "utf8")+msg)
# if __name__ == "__main__":
#     SERVER.listen(5)  # Listens for 5 connections at max.
#     print("Waiting for connection...")
#     ACCEPT_THREAD = Thread(target=accept_incoming_connections)
#     ACCEPT_THREAD.start()  # Starts the infinite loop.
#     ACCEPT_THREAD.join()
#     SERVER.close()