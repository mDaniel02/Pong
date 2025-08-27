import socket

DISCOVERY_PORT = 37020
DISCOVERY_MSG = b"DISCOVER_PONG_SERVER"
RESPONSE_MSG = b"PONG_SERVER_HERE"

def discovery_server():
    """Server-side: listen for UDP discovery requests and reply."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", DISCOVERY_PORT))
    print("[Discovery] Server listening for discovery requests...")
    while True:
        data, addr = sock.recvfrom(1024)
        if data == DISCOVERY_MSG:
            print(f"[Discovery] Received discovery from {addr}, replying...")
            sock.sendto(RESPONSE_MSG, addr)

def discover_server(timeout=3):
    """Client-side: broadcast discovery message and wait for server reply."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    sock.sendto(DISCOVERY_MSG, ('<broadcast>', DISCOVERY_PORT))
    print("[Discovery] Broadcast sent, waiting for server response...")

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            if data == RESPONSE_MSG:
                print(f"[Discovery] Found server at {addr[0]}")
                return addr[0]
    except socket.timeout:
        print("[Discovery] No server found on LAN.")
        return None