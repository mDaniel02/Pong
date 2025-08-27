import pygame
import threading
import time
from network import NetworkClient
from player import Players, Ball, WinCondition
from Scoreboard import GameStatsManager

WindowWidth = 1920
WindowHeight = 1080
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
screen = pygame.display.set_mode((WindowWidth, WindowHeight))


class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.is_paused = False
        self.font = pygame.font.SysFont(None, 100)

    def toggle(self):
        self.is_paused = not self.is_paused

    @property
    def paused(self):
        return self.is_paused

    def draw(self):
        if self.is_paused:
            
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) 
            self.screen.blit(overlay, (0, 0))

            
            text = self.font.render("Paused", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(text, text_rect)


class MultiplayerNameInputScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.surfaceText = ""
        self.running = True

    def draw(self):
        self.screen.fill(BLACK)
        prompt = self.font.render("Enter your name:", True, WHITE)
        input_surface = self.font.render(self.surfaceText, True, WHITE)
        self.screen.blit(prompt, (WindowWidth // 2 - prompt.get_width() // 2, WindowHeight // 3))
        self.screen.blit(input_surface, (WindowWidth // 2 - input_surface.get_width() // 2, WindowHeight // 2))
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.surfaceText = self.surfaceText[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.surfaceText.strip():
                        self.running = False
                else:
                    if len(self.surfaceText) < 15:
                        self.surfaceText += event.unicode

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
        return self.surfaceText.strip()

class MultiplayerGame:
    def __init__(self, screen, server_ip=None):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.player1 = Players(0, 0, 20, 250, 10, WHITE)
        self.player2 = Players(WindowWidth - 30, 0, 20, 250, 10, WHITE)
        self.ball = Ball(WindowWidth // 2, WindowHeight // 2, 9, 7, WHITE)

        self.is_server = server_ip is None

        self.wincondition = WinCondition(max_score=3)
        self.game_over = False
        self.winner_text = ""

        self.player1_name = ""
        self.player2_name = ""

        if self.is_server:
            from server import Server
            self.server = Server()
            threading.Thread(target=self.server.run, daemon=True).start()
            self.score1 = 0
            self.score2 = 0
            self.pause_menu = PauseMenu(screen)
        else:
            self.client = NetworkClient(server_ip)
            self.score1 = 0
            self.score2 = 0
            self.pause_menu = PauseMenu(screen)

        self.paused = False 

    def wait_for_clients(self):
        font = pygame.font.SysFont(None, 48)
        clock = pygame.time.Clock()

        while self.server.connected_players < 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.screen.fill(BLACK)
            text = font.render(f"Waiting for Player 2 ... ({self.server.connected_players}/2)", True, WHITE)
            self.screen.blit(text, (WindowWidth // 2 - 300, WindowHeight // 2))
            pygame.display.flip()
            clock.tick(30)

    def show_connection_success_screen(self):
        font = pygame.font.SysFont(None, 48)
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < 2000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.screen.fill(BLACK)
            text = font.render("Connected! Starting game...", True, WHITE)
            self.screen.blit(text, (WindowWidth // 2 - 200, WindowHeight // 2))
            pygame.display.flip()
            clock.tick(60)

    def exchange_names(self):
        input_screen = MultiplayerNameInputScreen(self.screen)

        if self.is_server:
            self.player1_name = input_screen.run() or "Player 1"
            print("[Server] Waiting for client name...")
            while not hasattr(self.server, 'client_name') or not self.server.client_name:
                time.sleep(0.1)
            self.player2_name = self.server.client_name or "Player 2"
            print(f"[Server] Got client name: {self.player2_name}")
        else:
            self.player2_name = input_screen.run() or "Player 2"
            print("[Client] Sending name to server...")
            response = self.client.send_name(self.player2_name)
            if response and isinstance(response, dict):
                self.player1_name = response.get("player1_name", "Player 1")
                self.player2_name = response.get("player2_name", "Player 2")
                print(f"[Client] Received names: {self.player1_name}, {self.player2_name}")

    def send_state(self):
        if self.is_server:
            keys = pygame.key.get_pressed()
            if not self.pause_menu.is_paused:
                if keys[pygame.K_w]:
                    self.player1.update(-1)
                elif keys[pygame.K_s]:
                    self.player1.update(1)

                self.player1.posy = max(0, min(WindowHeight - self.player1.height, self.player1.posy))

                self.server.player1.posy = self.player1.posy
                self.server.player1.playerRect = pygame.Rect(
                    self.server.player1.posx,
                    self.server.player1.posy,
                    self.server.player1.width,
                    self.server.player1.height
                )

                point = self.ball.update()
                if point != 0:
                    if point == 1:
                        self.score2 += 1
                    elif point == -1:
                        self.score1 += 1
                    self.ball.reset()
                    self.ball.speed = 7

            self.server.ball.posx = self.ball.posx
            self.server.ball.posy = self.ball.posy

            self.player2.posy = self.server.player2_pos
            self.player2.playerRect = pygame.Rect(
                self.player2.posx,
                self.player2.posy,
                self.player2.width,
                self.player2.height
            )
            self.server.score1 = self.score1
            self.server.score2 = self.score2
            self.paused = self.server.pause_state

        else:
            keys = pygame.key.get_pressed()
            if not self.pause_menu.is_paused:
                if keys[pygame.K_UP]:
                    self.player2.update(-1)
                elif keys[pygame.K_DOWN]:
                    self.player2.update(1)

            data = {"paddle_pos": self.player2.posy}
            try:
                response = self.client.send(data)
                if not response:
                    print("[Client] No response from server.")
                    self.running = False  
                    return
            except Exception as e:
                print(f"[Client] Send error: {e}")
                self.running = False  
                return

            self.player1.posy = response.get("player1_paddle_pos", self.player1.posy)
            self.player1.playerRect = pygame.Rect(
                self.player1.posx,
                self.player1.posy,
                self.player1.width,
                self.player1.height
            )

            self.player2.posy = response.get("player2_paddle_pos", self.player2.posy)
            self.player2.playerRect = pygame.Rect(
                self.player2.posx,
                self.player2.posy,
                self.player2.width,
                self.player2.height
            )

            self.ball.posx = response.get("ball_posx", self.ball.posx)
            self.ball.posy = response.get("ball_posy", self.ball.posy)

            self.score1 = response.get("score1", self.score1)
            self.score2 = response.get("score2", self.score2)

            self.paused = response.get("pause_state", False)

    def run(self):
        if self.is_server:
            self.wait_for_clients()
        else:
            self.show_connection_success_screen()

        self.exchange_names()

        ListOfPlayers = [self.player1, self.player2]
        font = pygame.font.SysFont(None, 48)
        winner_font = pygame.font.SysFont(None, 96)
        count = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause_menu.toggle()

                        if self.is_server:
                            self.server.send_pause_toggle()
                        else:
                            try:
                                self.client.send({"type": "pause_toggle"})
                            except Exception as e:
                                print(f"[Client] Failed to send pause toggle: {e}")
                                self.running = False  
                                
                    if self.game_over and event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit()

            if not self.game_over and not self.pause_menu.is_paused:
                for player in ListOfPlayers:
                    if pygame.Rect.colliderect(self.ball.getRect(), player.getRect()):
                        self.ball.hit()
                        self.ball.speed *= 1.05

            if not self.game_over:
                self.send_state()
                if not self.running:
                    break 

                self.game_over, self.winner_text = self.wincondition.check_winner(self.score1, self.score2)

            if self.game_over:
                player_name = (
                    self.player1_name if "Player 1" in self.winner_text
                    else self.player2_name if "Player 2" in self.winner_text
                    else "Unknown"
                )
                game = "Pong Multiplayer"
                winner_stats = [player_name, 1, game]
                stat_manager = GameStatsManager()

                if count:
                    stat_manager.update_stats(winner_stats)
                    print("Winner Stats:", winner_stats)
                    count = False

            self.screen.fill(BLACK)

            if not self.game_over:
                self.player1.display()
                self.player2.display()
                self.ball.display()

                self.player1.displayScore(self.score1, WindowWidth / 2 - 40, 20, WHITE)
                self.player2.displayScore(self.score2, WindowWidth / 2 + 40, 20, WHITE)

                p1_text = font.render(self.player1_name, True, WHITE)
                p2_text = font.render(self.player2_name, True, WHITE)
                self.screen.blit(p1_text, (20, 20))
                self.screen.blit(p2_text, (WindowWidth - p2_text.get_width() - 20, 20))

                if self.pause_menu.is_paused:
                    self.pause_menu.draw()
            else:
                self.screen.fill(BLACK)
                winner_surface = winner_font.render(self.winner_text, True, WHITE)
                instruction_surface = font.render("Press ESC to return to mode selection", True, WHITE)

                self.screen.blit(winner_surface, ((WindowWidth - winner_surface.get_width()) // 2,
                                                  (WindowHeight // 2) - winner_surface.get_height()))
                self.screen.blit(instruction_surface, ((WindowWidth - instruction_surface.get_width()) // 2,
                                                       (WindowHeight // 2) + 20))

            pygame.display.flip()
            self.clock.tick(self.FPS)

            if self.is_server and not self.server.running:
                print("[Server] Client disconnected. Returning to menu.")
                self.running = False
                self.server.shutdown()

        return True