import socket
import os
import threading

ServerIP = "170.187.157.166"
ServerPort = 12001
ADDRESS = (ServerIP, ServerPort)

# Store all current client connections
client_connections = []
# Store the number of active connections
active_connections = 0


# Create a socket
try:
    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print (f'Unable to establish a socket connection {err}\n')

# Bind the socket to the port
try:
    ServerSocket.bind((ADDRESS))
except socket.error as err:
    print (f'Unable to bind to the server {err}\n')

# Function to handle each client connection in a separate thread
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] Connection added at: {addr}.")

    # Add the connection to the list of connections
    client_connections.append(conn)
    
    connected = True
    
    try:
        while connected:
            # Listen for messages
            msg = conn.recv(1024).decode()
            
            # Print the message and address of client
            print("From: " + str(addr))
            print(str(msg))

            # Send new messages to all clients
            broadcast(msg)

            # # Disconnect if the client sends the disconnect message
            # if msg == DISCONNECT_MESSAGE:
            #     connected = False

            # Close the connection if the client has closed the connection
            if not msg:
                break
    except:
        print(f"[CONNECTION LOST] Connection lost at: {addr}.")
        
    conn.close()
    print(f"[CONNECTION CLOSED] Connection closed at: {addr}.")
    # Remove the connection from the list of connections
    client_connections.remove(conn)
    # Update the number of active connections
    active_connections = threading.active_count() - 2
    print("[ACTIVE CONNECTIONS] " + str(active_connections))


# Function to broadcast message to all clients
def broadcast(msg):
    # Iterate through current list of clients
    for conn in client_connections:
        conn.send(msg.encode())


# Function to start the server, create a thread for every new connection
def start():
    # Start listening for connections
    ServerSocket.listen()
    print(f"[LISTENING] Server is listening on {ServerIP}")
    while True:
        # Store connection details, create a thread for each connection
        conn, addr = ServerSocket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        active_connections = threading.active_count() - 1
        print("[ACTIVE CONNECTIONS] " + str(active_connections))


print ("[STARTING] Server has started")
start()