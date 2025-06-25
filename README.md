# TCP Chat Room

A command-line chat room built using TCP sockets in Python, with admin features for kicking, banning, and managing users.
## 🚀 Features

- 🔗 Multi-client chat via TCP
- 🔐 Admin authentication
- 🦶 Kick and ban users
- ✅ Simple, command-line interface

## 📂 File Structure
```
├── server.py # Runs the chat server
├── client.py # Connects a client to the chat room
└── bans.txt # Stores banned usernames
```
## 🧑‍💻 Getting Started

### 🔧 Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/note-9/TCPChat
   cd TCPChat
   ```
Run the Server
```bash
python server.py
```
Connect Clients
In separate terminals:
```bash
python client.py
```
You can adjust the host and port in both server.py and client.py if needed.

📜 Commands
```
/kick <user>	# Disconnect a user
/ban <user>	# Kick and prevent the user from joining
/exit	# Leave the chat
```
⚠️ Disclaimer

This is an educational project meant for learning about:

    Sockets

    Threading

    Basic client-server architecture

It is not secure for production use. There's no encryption, proper authentication, or error handling.
