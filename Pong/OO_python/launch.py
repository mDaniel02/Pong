import pygame
from network import discover_server
from multiplayer_game import MultiplayerGame

def run_launch(screen):
    print("[Launch] Searching for server on LAN...")
    server_ip = discover_server()

    if server_ip:
        print(f"[Launch] Found server at {server_ip}. Connecting as client...")
        game = MultiplayerGame(screen, server_ip=server_ip)
    else:
        print("[Launch] No server found. Starting as server...")
        game = MultiplayerGame(screen)

    result = game.run()  

    if result: 
        return "back"
    return "quit"

if __name__ == "__main__":
    pygame.init()