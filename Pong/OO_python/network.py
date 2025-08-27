import socket
import pickle
import threading

PORT = 5555
DISCOVERY_PORT = 5556
DISCOVERY_MSG = b"DISCOVER_PONG_SERVER"

class NetworkClient:
    def __init__(self, server_ip, port=PORT):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (server_ip, port)
        self.client.connect(self.addr)
        self.lock = threading.Lock()

    def send(self, data):
        try:
            self.lock.acquire()
            self.client.sendall(pickle.dumps(data))
            reply = self.client.recv(4096)
            self.lock.release()
            return pickle.loads(reply)
        except Exception as e:
            self.lock.release()
            print(f"[Client Error] {e}")
            return None

    def send_name(self, player_name):
        try:
            self.lock.acquire()
            data = {"type": "name", "name": player_name}
            self.client.sendall(pickle.dumps(data))
            reply = self.client.recv(4096)
            self.lock.release()
            return pickle.loads(reply)
        except Exception as e:
            self.lock.release()
            print(f"[Client Error - send_name] {e}")
            return None

    def receive_names(self):
        try:
            data = self.client.recv(4096)
            return pickle.loads(data)
        except Exception as e:
            print(f"[Client Error - receive_names] {e}")
            return None

def discover_server(timeout=3):
    """Broadcast UDP to find server IP on LAN."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = DISCOVERY_MSG
    sock.sendto(message, ('<broadcast>', DISCOVERY_PORT))

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            if data == DISCOVERY_MSG:
                print(f"[Discovery] Found server at {addr[0]}")
                return addr[0]
    except socket.timeout:
        return None