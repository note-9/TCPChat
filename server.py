import threading
import socket
from dotenv import load_dotenv
import os

load_dotenv()

admin_password = os.getenv("admin_password")

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
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('Kick'):
                if usernames[clients.index(client)] == 'admin':
                    kick_user(msg.decode('ascii')[5:])
                else:
                    client.send("Command was refused!".encode('ascii'))
            elif msg.decode('ascii').startswith('Ban'):
                if usernames[clients.index(client)] == 'admin':
                    kick_user(msg.decode('ascii')[4:])
                    with open('bans.txt', 'a') as f:
                        f.write(f'{msg.decode('ascii')[4:]}\n')
                    print(f'{msg.decode('ascii')[4:]} was banned!')
                else:
                    client.send("Command was refused!".encode('ascii'))
            else:
                broadcast(message)
        except:
            if client in clients:
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
        
        with open('bans.txt', 'r') as f:
            bans = f.readlines()

        if username+'\n' in bans:
            client.send('Ban'.encode('ascii'))
            client.close()
            continue

        if username == "admin":
            client.send("Password".encode('ascii'))
            password = client.recv(1024).decode('ascii')

            if password != admin_password:
                client.send('Refuse'.encode('ascii'))
                client.close()
                continue

        usernames.append(username)
        clients.append(client)

        print(f"Username of the client is {username}")
        broadcast(f"{username} has joined the chat!".encode('ascii'))
        client.send("Connected to the server".encode('ascii'))

        thread = threading.Thread(target = handle, args = (client,))
        thread.start()

def kick_user(name):
    if name in usernames:
        name_idx = usernames.index(name)
        client_to_kick = clients[name_idx]
        clients.remove(client_to_kick)
        client_to_kick.send("You were kicked by an admin".encode('ascii'))
        client_to_kick.close()
        usernames.remove(name)
        broadcast(f"{name} was kicked by an admin!".encode('ascii'))

print("Server is Listening...")

recieve()
