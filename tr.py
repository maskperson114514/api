import socket
import struct
import random

# Tracker server settings
TRACKER_PORT = 6881

# Create a UDP socket for the tracker server
tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tracker_socket.bind(('', TRACKER_PORT))

# Function to handle announce requests from clients
def handle_announce(data, addr):
    print(f"Received announce request from {addr[0]}:{addr[1]}")

    # Parse the announce request
    info_hash = data[0:20]
    peer_id = data[20:36]
    downloaded = struct.unpack(">Q", data[36:44])[0]
    left = struct.unpack(">Q", data[44:52])[0]
    uploaded = struct.unpack(">Q", data[52:60])[0]
    event = data[60:64].decode()

    # Generate a random port number for the peer
    port = random.randint(1024, 65535)

    # Create the announce response
    response = b''
    response += info_hash
    response += peer_id
    response += struct.pack(">I", downloaded)
    response += struct.pack(">I", left)
    response += struct.pack(">I", uploaded)
    response += b'00000000'  # Reserved
    response += struct.pack(">I", 1)  # Number of seeders
    response += struct.pack(">I", 1)  # Number of leechers
    response += struct.pack(">I", port)  # Port number of the peer
    response += addr[0].encode()  # IP address of the peer
    response += struct.pack(">H", 0)  # Reserved

    # Send the announce response to the client
    tracker_socket.sendto(response, addr)

# Main loop
while True:
    # Receive data from a client
    data, addr = tracker_socket.recvfrom(1024)

    # Handle the announce request
    handle_announce(data, addr)

    # Print the client's public IP and port
    print(f"Client's public IP: {addr[0]}")
    print(f"Client's public port: {addr[1]}")
