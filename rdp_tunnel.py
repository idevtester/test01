# rdp_tunnel.py
import socket
import threading

# Function to forward traffic from source to destination
def forward_traffic(source_socket, destination_socket):
    while True:
        data = source_socket.recv(4096)
        if not data:
            break
        destination_socket.send(data)

# Function to start the tunnel
def start_tunnel(server_ip, server_port, local_ip, local_port, protocol):
    if protocol.upper() == 'TCP':
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif protocol.upper() == 'UDP':
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        raise ValueError("Unsupported protocol. Use 'TCP' or 'UDP'.")

    server_socket.connect((server_ip, server_port))

    if protocol.upper() == 'TCP':
        local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif protocol.upper() == 'UDP':
        local_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    local_socket.bind((local_ip, local_port))

    threading.Thread(target=forward_traffic, args=(server_socket, local_socket)).start()
    threading.Thread(target=forward_traffic, args=(local_socket, server_socket)).start()

if __name__ == "__main__":
    import sys
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    local_ip = sys.argv[3]
    local_port = int(sys.argv[4])
    protocol = sys.argv[5]

    start_tunnel(server_ip, server_port, local_ip, local_port, protocol)
