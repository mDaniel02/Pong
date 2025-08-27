import pygame
from select_mode import SelectGameMode
from player import run_local_game  
from launch import run_launch      

class GameLauncher:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            
            selector = SelectGameMode(self.screen)
            selector.run()
            selected_mode = selector.game_mode

            if selected_mode == "2_Player" or selected_mode == "BOT":
                result = run_local_game(self.screen, selected_mode)
            elif selected_mode == "Multiplayer":
                result = run_launch(self.screen)
            else:
                result = None

            if result == "back":
                continue

            if result == "quit" or selected_mode is None:
                self.running = False

        pygame.quit()

if __name__ == "__main__":
    GameLauncher().run()

