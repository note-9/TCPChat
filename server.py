import threading
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connection successfully created.")

host = '127.0.0.1'
port = 2345

s.bind((host, port))
s.listen()

clients = []
usernames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            idx = clients.index(client)
            clients.remove(idx)
            client.close()
            username = usernames[idx]
            broadcast(f"{username} has left the chat!".encode('ascii'))
            usernames.remove(username)
            break

def recieve():
    while True:
        client, address = s.accept()
        print(f"Connected with {str(address)}")

        client.send("User".encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        print(f"Username of the client is {username}")
        broadcast(f"{username} has joined the chat!".encode('ascii'))
        client.send("Connected to the server".encode('ascii'))

        thread = threading.Thread(target = handle, args = (client,))
        thread.start()

print("Server is Listening...")

recieve()
