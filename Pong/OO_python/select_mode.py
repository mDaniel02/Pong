import pygame

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
WINDOW_WIDTH = 1920 
WINDOW_HEIGHT = 1080

class SelectGameMode:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.game_mode = None
        self.running = True

    def draw(self):
        self.screen.fill((0, 0, 0))

        title_text = self.font.render("Choose Game Mode:", True, WHITE)
        mode1_text = self.font.render("1. 2-Player", True, GRAY)
        mode2_text = self.font.render("2. Play vs BOT", True, GRAY)
        mode3_text = self.font.render("3. Multiplayer", True, GRAY)

        self.screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 150))
        self.screen.blit(mode1_text, (WINDOW_WIDTH * 0.3 - mode1_text.get_width() // 2, 300))
        self.screen.blit(mode2_text, (WINDOW_WIDTH * 0.7 - mode2_text.get_width() // 2, 300))
        self.screen.blit(mode3_text, (WINDOW_WIDTH // 2 - mode3_text.get_width() // 2, 400))

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.game_mode = "2_Player"
                    self.running = False
                elif event.key == pygame.K_2:
                    self.game_mode = "BOT"
                    self.running = False
                elif event.key == pygame.K_3:
                    self.game_mode = "Multiplayer"
                    self.running = False

    def run(self):
        while self.running:
            self.draw()
            self.handle_events()
        print(self.game_mode)
        return self.game_mode