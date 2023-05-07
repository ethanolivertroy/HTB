import socket

# Define the host and port to scan
host = '172.16.22.1'
port = 5985

# Check if the port is open
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Set a timeout of 1 second to avoid hanging on closed ports
    s.settimeout(1)
    try:
        s.connect((host, port))
        print(f"Port {port} is open")
    except (socket.timeout, ConnectionRefusedError):
        print(f"Port {port} is not open")

