import socket
import threading

username = input("Choose a Username: ")
if username == 'admin':
    password = input("Enter password for admin: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 2345))

stop_thread = False

def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == "User":
                client.send(username.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'Password':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'Refuse':
                        print("Connection was refused! Worng password!")
                        stop_thread = True
                elif next_message == 'Ban':
                    print("Connection refused beacuse of ban!")
                    client.close()
                    stop_thread = True
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        if stop_thread == True:
            break

        message = f"{username}: {input('')}"
        if message[len(username)+2:].startswith('/'):
            if username == 'admin':
                if message[len(username)+2:].startswith("/kick"):
                    client.send(f'Kick {message[len(username)+2+6:]}'.encode('ascii'))
                elif message[len(username)+2:].startswith("/ban"):
                    client.send(f'Ban {message[len(username)+2+5:]}'.encode('ascii'))
            else:
                print("Commands can only be executed by admin!")
        else:
            client.send(message.encode('ascii'))
        
recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
