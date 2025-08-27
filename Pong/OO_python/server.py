import socket
import threading
import pickle
import pygame
from player import Players, Ball
import time

pygame.init()

PORT = 5555
DISCOVERY_PORT = 5556
DISCOVERY_MSG = b"DISCOVER_PONG_SERVER"
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

class Server:
    def __init__(self):
        # TCP socket for game connection
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', PORT))
        self.server.listen(1)
        print("[Server] Waiting for a client to connect...")
        self.connected_players = 1

        # UDP socket for discovery
        self.discovery_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.discovery_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.discovery_sock.bind(('', DISCOVERY_PORT))
        threading.Thread(target=self.discovery_responder, daemon=True).start()

        self.client_conn = None
        self.client_addr = None

        # Game objects
        self.player1 = Players(50, 250, 20, 100, 7, (255, 255, 255))
        self.player2_pos = 250
        self.ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 9, 7, (255, 255, 255))

        self.score1 = 0
        self.score2 = 0

        self.running = True
        self.pause_state = False  # Shared pause state

        # For name exchange
        self.client_name = None
        self.player1_name = "Player 1"  
        self.names_sent = False

    def discovery_responder(self):
        while True:
            try:
                data, addr = self.discovery_sock.recvfrom(1024)
                if data == DISCOVERY_MSG:
                    print(f"[Server] Discovery ping from {addr}, replying.")
                    self.discovery_sock.sendto(DISCOVERY_MSG, addr)
            except Exception as e:
                print(f"[Server] Discovery responder error: {e}")

    def accept_client(self):
        self.client_conn, self.client_addr = self.server.accept()
        print(f"[Server] Client connected from {self.client_addr}")

    def send_pause_toggle(self):
        try:
            msg = pickle.dumps({"type": "pause_toggle"})
            self.client_conn.sendall(msg)
            print("[Server] Sent pause toggle to client")
        except Exception as e:
            print(f"[Server] Error sending pause toggle: {e}")

    def handle_client(self):
        while self.running:
            try:
                data = self.client_conn.recv(4096)
                if not data:
                    print("[Server] Client disconnected")
                    self.running = False
                    break

                client_data = pickle.loads(data)

                # Handle name exchange
                if isinstance(client_data, dict) and client_data.get("type") == "name":
                    self.client_name = client_data.get("name", "Player 2")
                    print(f"[Server] Received client name: {self.client_name}")

                    while not hasattr(self, "player1_name") or self.player1_name.strip() == "":
                        time.sleep(0.1)

                    names_data = {
                        "player1_name": self.player1_name,
                        "player2_name": self.client_name,
                    }
                    self.client_conn.sendall(pickle.dumps(names_data))
                    self.names_sent = True
                    continue

                # Handle pause toggle request from client
                if client_data.get("type") == "pause_toggle":
                    self.pause_state = not self.pause_state
                    print(f"[Server] Received pause toggle from client. New state: {self.pause_state}")
                    self.send_pause_toggle() 
                    continue

                # Update player2 paddle position from client
                self.player2_pos = client_data.get("paddle_pos", self.player2_pos)

                # Update ball and scores only if NOT paused
                if not self.pause_state:
                    point = self.ball.update()
                    if point == 1:
                        self.score2 += 1
                        self.ball.reset()
                        self.ball.speed = 7
                    elif point == -1:
                        self.score1 += 1
                        self.ball.reset()
                        self.ball.speed = 7

                game_state = {
                    "player1_paddle_pos": self.player1.posy,
                    "player2_paddle_pos": self.player2_pos,
                    "ball_posx": self.ball.posx,
                    "ball_posy": self.ball.posy,
                    "score1": self.score1,
                    "score2": self.score2,
                    "pause_state": self.pause_state
                }

                self.client_conn.sendall(pickle.dumps(game_state))

            except Exception as e:
                print(f"[Server] Client connection error: {e}")
                self.running = False
                break

    def update_game(self):
        if not self.pause_state:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player1.update(-1)
            elif keys[pygame.K_s]:
                self.player1.update(1)

            if self.player1.posy < 0:
                self.player1.posy = 0
            elif self.player1.posy > WINDOW_HEIGHT - self.player1.height:
                self.player1.posy = WINDOW_HEIGHT - self.player1.height

            self.player1.playerRect = pygame.Rect(
                self.player1.posx, self.player1.posy, self.player1.width, self.player1.height
            )
    def shutdown(self):
        self.running = False
        try:
            if self.client_conn:
                self.client_conn.shutdown(socket.SHUT_RDWR)
                self.client_conn.close()
        except Exception as e:
            print(f"[Server] Error closing client connection: {e}")

        try:
            self.server.close()
        except Exception as e:
            print(f"[Server] Error closing main server socket: {e}")

        try:
            self.discovery_sock.close()
        except Exception as e:
            print(f"[Server] Error closing discovery socket: {e}")

        print("[Server] Shutdown complete.")

    def run(self):
        self.accept_client()
        self.connected_players += 1
        threading.Thread(target=self.handle_client, daemon=True).start()
        clock = threading.Event()

        while self.running:
            self.update_game()
            clock.wait(1 / 60)

if __name__ == "__main__":
    server = Server()
    server.run()