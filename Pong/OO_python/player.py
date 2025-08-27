import pygame, time, csv, os
from Scoreboard import GameStatsManager


pygame.init()

# colors
BLACK = ( 0, 0, 0)
WHITE   = ( 255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0, 120 , 215)
FONT = pygame.font.Font(None, 36)
game_font = pygame.font.SysFont(None, 30)
WindowWidth = 1920  
WindowHeight = 1080

game = "Pong"

size = (WindowWidth, WindowHeight)
screen = pygame.display.set_mode((WindowWidth, WindowHeight))
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Pong")


clock = pygame.time.Clock()

bot_enabled = True

class Players:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.playerRect = pygame.Rect(posx, posy, width, height)
        self.player = pygame.draw.rect(screen, self.color, self.playerRect)

    def display(self):
        self.player = pygame.draw.rect(screen, self.color, self.playerRect)

    def update(self, yFac):
        self.posy = self.posy + self.speed*yFac

        if self.posy <= 0:
            self.posy = 0
        elif self.posy + self.height >= WindowHeight:
            self.posy = WindowHeight-self.height

        self.playerRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def displayScore(self, score, x, y, color):
        score_text = FONT.render(str(score), True, color)
        scoreRect = score_text.get_rect()
        scoreRect.center = (x, y)

        screen.blit(score_text, scoreRect)

    def getRect(self):
        return self.playerRect
    
    def get_state(self):
        return self.posy

    def set_state(self, y):
        self.posy = y
        self.playerRect = pygame.Rect(self.posx, self.posy, self.width, self.height)
    
  

class BotPlayer(Players):
    def __init__(self, posx, posy, width, height, speed, color):
        super().__init__(posx, posy, width, height, speed, color)

    def auto_move(self, ball):
        
        velx = ball.speed * ball.xFac
        vely = ball.speed * ball.yFac

        
        if velx > 0:
            # Estimate time until ball reaches the bot's paddle (x-position)
            time_to_reach = (self.posx - ball.posx - ball.radius) / velx

            # Predict future Y position
            predicted_y = ball.posy + vely * time_to_reach

            # Handle bouncing off the top and bottom of the screen
            while predicted_y < 0 or predicted_y > WindowHeight:
                if predicted_y < 0:
                    predicted_y = -predicted_y
                elif predicted_y > WindowHeight:
                    predicted_y = 2 * WindowHeight - predicted_y

            # Move bot paddle toward predicted Y
            paddle_center = self.posy + self.height / 2

            if paddle_center < predicted_y:
                self.update(1)
            elif paddle_center > predicted_y:
                self.update(-1)
            else:
                self.update(0)
        else:
            # Ball is going away from the bot; stay still
            self.update(0)




class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(
        screen, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1

    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.speed*self.xFac
        self.posy += self.speed*self.yFac


        if self.posy < 0 + self.radius or self.posy > WindowHeight - self.radius:
            self.yFac *= -1

        if self.posx < 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx > WindowWidth and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        self.posx = WindowWidth//2
        self.posy = WindowHeight//2
        self.xFac *= -1
        self.firstTime = 1
        time.sleep(0.5)

    def hit(self):
        self.xFac *= -1

    def getRect(self):
        return self.ball
    


class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.pause_text = self.font.render("Paused - Press Space to continue", True, (255, 255, 255))
        self.quit_text = self.font.render("Quit     - Press Q to quit", True, (255, 255, 255))
        self.bot_text = self.font.render("BOT       - Press b to toggle bot", True, (255, 255, 255))
        self.is_paused = False

    def toggle(self):
        self.is_paused = not self.is_paused

    def run(self):
        while self.is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.toggle()
                    if event.key == pygame.K_q:
                        pygame.quit()
                


            self.screen.fill((0, 0, 0))
            self.screen.blit(self.quit_text, (WindowWidth // 2 - self.pause_text.get_width(), WindowHeight//2))
            self.screen.blit(self.bot_text, (WindowWidth // 2 - self.pause_text.get_width(), WindowHeight//2 - self.bot_text.get_height() -5))            
            self.screen.blit(self.pause_text, (WindowWidth // 2 - self.pause_text.get_width(), WindowHeight//2 - (self.bot_text.get_height() + self.pause_text.get_height()) - 5 ))
            pygame.display.update()
            clock.tick(60)


class WinCondition:
    def __init__(self, max_score=5):
        self.max_score = max_score
        self.winner = None
        self.font = pygame.font.Font(None, 48)
        self.winner_display_time = 180

    def check(self, p1_score, p2_score):
        if p1_score >= self.max_score:
            self.winner = "Player 1 wins"
            return True, self.winner
        elif p2_score >= self.max_score:
            self.winner = "Player 2 wins"
            return True, self.winner
        return False

    def check_winner(self, p1_score, p2_score):
        if p1_score >= self.max_score:
            self.winner = "Player 1 wins"
            return True, self.winner
        elif p2_score >= self.max_score:
            self.winner = "Player 2 wins"
            return True, self.winner
        else:
            return False, ""

    def draw_winner(self, screen):
        if self.winner and self.winner_display_time > 0:
            text = self.font.render(self.winner, True, WHITE)
            text_rect = text.get_rect(center=(WindowWidth // 2, WindowHeight // 2))
            screen.blit(text, text_rect)
            self.winner_display_time -= 1

    def reset(self):
        self.winner = None
        self.winner_display_time = 180






class NameSuggester:
    def __init__(self, filename="scoreboard.csv"):
        self.filename = filename

    def suggest_player_names(self, partial_name):
        suggestions = []
        if not os.path.exists(self.filename):
            return suggestions
        
        with open(self.filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                player_name = row[0]  
                if partial_name.lower() in player_name.lower():  
                    suggestions.append(player_name)
        
        return suggestions
    

class NameInputScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.is_running = True
        self.active_player = 1
        self.surfaceText = ""
        self.player1_name = ""
        self.player2_name = ""
        self.running = True
        self.name_suggester = NameSuggester()  
        self.suggestions = []  

    def draw(self):
        self.screen.fill(BLACK)

        prompt = self.font.render(f"Enter Player {self.active_player}'s Name:", True, WHITE)
        input_surface = self.font.render(self.surfaceText, True, WHITE)

        self.screen.blit(prompt, (WindowWidth // 2 - prompt.get_width() // 2, WindowHeight // 3))
        self.screen.blit(input_surface, (WindowWidth // 2 - input_surface.get_width() // 2, WindowHeight // 2))

        if self.suggestions:
            suggestion_y_pos = WindowHeight // 2 + 100  
            for idx, suggestion in enumerate(self.suggestions, start=1):
                suggestion_text = self.font.render(f"{idx}. {suggestion}", True, WHITE)
                self.screen.blit(suggestion_text, (WindowWidth // 2 - suggestion_text.get_width() // 2, suggestion_y_pos + (idx - 1) * 40))

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
                    if self.active_player == 1:
                        self.player1_name = self.surfaceText
                        self.surfaceText = ""
                        self.active_player = 2
                    else:
                        self.player2_name = self.surfaceText
                        self.running = False  
                else:
                    if len(self.surfaceText) < 15: 
                        self.surfaceText += event.unicode

                self.suggestions = self.name_suggester.suggest_player_names(self.surfaceText)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
        return self.player1_name, self.player2_name


from select_mode import SelectGameMode


def run_local_game(screen, selected_mode):
    running = True
    bot_enabled = False
    pause_menu = PauseMenu(screen)

    name_screen = NameInputScreen(screen)
    player1_name, player2_name = "", ""

    print(f"Player 1: {player1_name}, Player 2: {player2_name}")

    SelectGameMode.game_mode = selected_mode

    print(selected_mode)

    if selected_mode == "2_Player":
        print("2 Player")  
        player1, player2 = name_screen.run()
        print(player1, player2)
    elif selected_mode == "BOT":
        print("BOT")
        bot_enabled = True


    # Defining the objects
    Player1 = Players(0, 0, 20, 250, 10, WHITE)
    
    
    
    Player2 = Players(WindowWidth-30, 0, 20, 250, 10, WHITE)
    bot_paddle = BotPlayer(WindowWidth-30, 0, 20, 250, 15, BLUE)
    ball = Ball(WindowWidth//2, WindowHeight//2, 9, 7, WHITE)
    

    if bot_enabled:
        ListOfPlayers = [Player1, bot_paddle]
    else: 
        ListOfPlayers = [Player1, Player2]
    
    Players.speed = 2
    # Initial parameters of the players
    score1, score2 = 0, 0
    Player1YFac, Player2YFac = 0, 0

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    Player2YFac = -Players.speed
                if event.key == pygame.K_DOWN:
                    Player2YFac = +Players.speed
                if event.key == pygame.K_w:
                    Player1YFac = -Players.speed
                if event.key == pygame.K_s:
                    Player1YFac = +Players.speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    Player2YFac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    Player1YFac = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause_menu.toggle()
                while pause_menu.is_paused:
                    pause_menu.run()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    bot_enabled = not bot_enabled
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                      
                    running=False
            
                    

        # Collision detection
        for Player in ListOfPlayers:
            if pygame.Rect.colliderect(ball.getRect(), Player.getRect()):
                ball.hit()
                ball.speed *= 1.05


        if bot_enabled:
            bot_paddle.auto_move(ball)  
        else:
            pass

        # Updating the objects
        Player1.update(Player1YFac)
        Player2.update(Player2YFac)
        point = ball.update()    
                

        if point == -1:
            score1 += 1
        elif point == 1:
            score2 += 1

        if point: 
            time.sleep(0.2)  
            ball.reset()
            ball.speed = 7


        winner_stats = []
        win_condition = WinCondition()

        stat_manager = GameStatsManager()

        
        if bot_enabled == False:
            if win_condition.check(score1, score2):
                if win_condition.winner == "Player 1 wins" and selected_mode =="2_Player":
                    winner_stats = [player1, 1, game]
                    stat_manager.update_stats([winner_stats[0], winner_stats[1], winner_stats[2]])
                    print(winner_stats)
                elif win_condition.winner == "Player 2 wins" and selected_mode =="2_Player":
                    winner_stats = [player2, 1, game]
                    print(winner_stats) 
                score1 = 0 
                score2 = 0
                win_condition.reset()
            

        if bot_enabled:
            if score1 or score2 == 10:
                score1, score2 = 0, 0

        # Displaying the objects on the screen
        Player1.display()
        if not bot_enabled:
            Player2.display()
        ball.display()
        if bot_enabled:
            bot_paddle.display()

        if bot_enabled:
            Player1.displayScore(score1,WindowWidth / 2 -80 / 2, 20, BLUE)
            Player2.displayScore(score2, WindowWidth / 2 +80 / 2, 20, BLUE)
        else:
            Player1.displayScore(score1,WindowWidth / 2 -80 / 2, 20, WHITE)
            Player2.displayScore(score2, WindowWidth / 2 +80 / 2, 20, WHITE)            

        pygame.display.update()
        clock.tick(60)     


if __name__ == "__main__":
    run_local_game()
    pygame.quit()
    