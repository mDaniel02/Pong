import pygame, time, csv

#initialisiere Pong


pygame.init()

# colors
BLACK = ( 0, 0, 0)
WHITE   = ( 255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0, 120 , 215)
FONT = pygame.font.Font(None, 36)

WindowWidth = 1920  
WindowHeight = 1080


size = (WindowWidth, WindowHeight)
screen = pygame.display.set_mode((WindowWidth, WindowHeight))
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Pong")


clock = pygame.time.Clock()



#Define Player variables


 

player_names = ["", ""]
active_player = 0


def main_menu_loop():
    running = True
    while running:
        

        name1 = FONT.render(player_names[0], True, WHITE)
        name2 = FONT.render(player_names[1], True, WHITE)
        screen.blit(name1, (20, 20))
        screen.blit(name2, (WindowWidth - name2.get_width() -20, 20))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(30) 
        time.sleep(2)
        running = False
        return (player_names)

def draw_input_screen():
    screen.fill(BLACK)

    input_text = FONT.render(f"Enter Player {active_player + 1} Name:", True, WHITE)
    screen.blit(input_text, (WindowWidth // 2 - 140, WindowHeight // 2 + 5))
    surface_text = FONT.render(player_names[active_player], True, (255,255,255))
    screen.blit(surface_text, (WindowWidth // 2 + 150, WindowHeight // 2 + 5))

    pygame.display.flip()

#name_input_loop()


def name_input_loop():
    global active_player
    while active_player < 2:
        draw_input_screen()
        for event in pygame.event.get():
            if event.type ==pygame.KEYDOWN:
                
                if event.key == pygame.K_RETURN:
                    active_player +=1
                elif event.key == pygame.K_BACKSPACE:
                    player_names[active_player] = player_names[active_player][:-1]
                else:
                    if len(player_names[active_player]) < 15:
                        player_names[active_player] += event.unicode


    clock.tick(30)
    pygame.display.flip()
    pygame.display.update()
    





PlayerWidth = 20
PlayerHeight = 90
PlayerSpeed = 10
PlayerColor = WHITE

Player_1_pos_x = 0
Player_1_pos_y = WindowHeight /2


Player_2_pos_x = WindowWidth - PlayerWidth
Player_2_pos_y = WindowHeight /2

#Draw Players
Player1 = pygame.draw.rect(screen, WHITE, [Player_1_pos_x, Player_1_pos_y, PlayerWidth, PlayerHeight])
Player2 = pygame.draw.rect(screen, WHITE, [Player_2_pos_x, Player_2_pos_y, PlayerWidth, PlayerHeight])


# Define ball position variables
ballpos_x = WindowWidth / 2
ballpos_y = WindowHeight / 2

BALL_SIZE = 20

BallMovement_x = 4
BallMovement_y = 4

ball = pygame.Rect(WindowWidth / 2 - BALL_SIZE / 2, WindowHeight / 2 - BALL_SIZE / 2, BALL_SIZE, BALL_SIZE)


#scoreboard variables
score1 = 0
score2  = 0
game_font = pygame.font.SysFont(None, 30)

win = 3

WinCount = 0

WinCountPlayer1 = 0
WinCountPlayer2 = 0




running = True


#paused game state

def show_start_screen():
    while True:
        screen.fill(BLACK)

        title = FONT.render("Chose Game Mode", True, WHITE)
        mode1 = FONT.render("1 - 2 Player", True, GRAY)
        mode2 = FONT.render("2 - vs BOT", True, GRAY)

        screen.blit(title, (250, 150))
        screen.blit(mode1, (300, 250))
        screen.blit(mode2, (300, 320))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "2 Player"
                elif event.key == pygame.K_2:
                    return "BOT"
        clock.tick(30)

mode = show_start_screen()
print("Selected mode:", mode)


paused = False

def pause_game():
    paused = True
    font = pygame.font.SysFont(None, 55)
    pause_text = font.render("Paused - press SPACE to continue", True, WHITE)
    screen.blit(pause_text, (WindowHeight / 2 -150, WindowWidth /2 ))
    bot_text = font.render("Bot - press B to toggle", True, WHITE)
    screen.blit(bot_text, (WindowHeight / 2 - 150 , WindowWidth /2 -100 ))
    restart_text = font.render("Restart - press R to restart", True, WHITE)
    screen.blit(restart_text, (WindowHeight / 2 - 150 , WindowWidth /2 -200 ))
    quit_text = font.render("Quit - press Q to quit", True, WHITE)
    screen.blit(quit_text, (WindowHeight / 2 - 150 , WindowWidth /2 -300 ))
    pygame.display.update()


    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    global bot_enabled
                    bot_enabled = not bot_enabled 
    
    clock.tick(10)
    pygame.display.flip()




                


bot_enabled = False
GameOver = False

if mode == "2 Player":
    name_input_loop()
    main_menu_loop()
    print("Player 1:", player_names[0])
    print("Player 2:", player_names[1])

if mode == "BOT":
    bot_enabled = True



csv_file = 'stats.csv'

game = ['Pong']
Player_1 = [player_names[0]]
Player_2 = [player_names[1]]

def write_result (Player_1, WinCountPlayer1, Player_2, WinCountPlayer2, game):
    try:
        with open(csv_file, mode='w', newline='') as file:
            file.seek(0)
            if file.tell() == 0:
                writer = csv.writer(file)
                writer.writerow([Player_1, WinCountPlayer1, Player_2, WinCountPlayer2, game])
                result = Player_1, WinCountPlayer1, Player_2, WinCountPlayer2, game
    except Exception as e:
        print('Error writing')
    return result


import Scoreboard
from Scoreboard import Player, PlayerLists

# Game loop
while running:
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause_game() 
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    bot_enabled = not bot_enabled


               

    if not GameOver:
        if score1 == win:
            WinCountPlayer1 +=1
            score1 = 0
            GameOver = True
            write_result(Player_1, WinCountPlayer1, Player_2, WinCountPlayer2, game)
            time.sleep(0.2)
            player1_list, player2_list = PlayerLists.read_game_results('stats.csv')
            PlayerStats = Scoreboard.Scoreboard.getStats(player1_list[0], player1_list[2])
            #p1 = Player(player1_list[0], player1_list[2], int (PlayerWins) + 1)
            #Scoreboard.Scoreboard.save(p1)
            if PlayerStats == "Player not found in Database!" or PlayerStats  == "Database created!":
                SavedPlayer = Player(player1_list[0], player1_list[2],player1_list[1])
                #SavedPlayer2 = Player(player2_list[0], player2_list[2],player2_list[1])
                Scoreboard.Scoreboard.save(SavedPlayer)
                #Scoreboard.Scoreboard.save(SavedPlayer2)
            else:
                PlayerWins = Scoreboard.Scoreboard.getStats(player1_list[0], "Pong")
                print(PlayerWins)
                p1 = Player(player1_list[0], player1_list[2], player1_list[1])
                Scoreboard.Scoreboard.save(p1)
            font = pygame.font.SysFont(None, 55)
            win_text = font.render("Win!", True, WHITE)
            screen.blit(win_text, (WindowHeight / 2 +100, WindowWidth /2 ))
            pygame.display.update()
            time.sleep(0.4)
            GameOver = False

            
        
        if score2 == win:
            WinCountPlayer2 +=1
            score2 = 0
            GameOver = True
            write_result(Player_1, WinCountPlayer1, Player_2, WinCountPlayer2, game)
            time.sleep(0.2)
            player1_list, player2_list = PlayerLists.read_game_results('stats.csv')
            print(player2_list[0], player2_list[2],player2_list[1])
            p2 = Player(player2_list[0],player2_list[2], player2_list[1])
            Scoreboard.Scoreboard.save(p2)
            font = pygame.font.SysFont(None, 55)
            win_text = font.render("Win!", True, WHITE)
            screen.blit(win_text, (WindowHeight / 2 + 700, WindowWidth /2 ))
            pygame.display.update()
            time.sleep(0.4)
            GameOver = False
            
            

        


    # Game logic
    
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, [WindowWidth / 2, 0], [WindowWidth / 2, WindowHeight], 5)

    # Objects
    pygame.draw.ellipse(screen, WHITE, ball)
    
    if bot_enabled:
        score_text = game_font.render(f"{score1}  {score2}", True, BLUE)
        screen.blit(score_text, (WindowWidth / 2 - score_text.get_width() / 2, 10))
    else:
        score_text = game_font.render(f"{score1}  {score2}", True, WHITE)
        screen.blit(score_text, (WindowWidth / 2 - score_text.get_width() / 2, 10))
        
    #Players

    pygame.draw.rect(screen, PlayerColor, Player1)
    pygame.draw.rect(screen, PlayerColor, Player2)


    #move the players
 

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and Player1.y > 0:
        Player1.y -= PlayerSpeed
    if keys[pygame.K_s] and Player1.y < WindowHeight - PlayerHeight:
        Player1.y += PlayerSpeed

    if keys[pygame.K_UP] and Player2.y > 0:
        Player2.y -= PlayerSpeed
    if keys[pygame.K_DOWN] and Player2.y < WindowHeight - PlayerHeight:
        Player2.y += PlayerSpeed

    

    # Ball movement
 


    ball.x += BallMovement_x
    ball.y += BallMovement_y


    #top, bottom ball collision
    if ball.y > WindowHeight - BALL_SIZE or ball.y < 0:
        BallMovement_y = BallMovement_y * -1

 

    #left, right side ball collision
    if ball.x > WindowWidth - BALL_SIZE:
        score1 +=1
        time.sleep(0.5)
        ball.x = WindowWidth / 2
        ball.y = WindowHeight / 2
        BallMovement_x = 4
        BallMovement_y = 4
        

    if ball.x < 0:
        score2 +=1
        time.sleep(0.5)
        ball.x = WindowWidth / 2
        ball.y = WindowHeight / 2
        BallMovement_x = 4
        BallMovement_y = 4


    #ball player collision
    if ball.colliderect(Player1) or ball.colliderect(Player2):
        BallMovement_x = BallMovement_x * -1.1


    #bot ball
    diff = ball.centery - Player2.centery

    if bot_enabled:
        if diff > 0 and Player2.bottom < WindowHeight:
           Player2.move_ip(0, min(PlayerSpeed, diff))
        elif diff < 0 and Player2.top >0:
            Player2.move_ip(0, max(-PlayerSpeed, diff))
           
       
        #if Player2.centery < ball.centery:
            #Player2.y += PlayerSpeed
        #elif Player2.centery > ball.centery:
            #Player2.y -= PlayerSpeed

    #Player2.y = max(0, min(Player2.y, WindowHeight - PlayerHeight))

        #if Player2.centery < ball.centery and Player2.bottom < WindowHeight:
           # Player2.move_ip(0, PlayerSpeed)
        #elif Player2.centery > ball.centery and Player2.top > WindowHeight:
            #Player2.move_ip(0, -PlayerSpeed)
        
    
#    if score1  == win:s
 #       WinCountPlayer1 +=1
  #      score1 = 0
#
 #   if score2  == win:
  #      WinCountPlayer2 +=1
   #     score2 = 0   
        

    #print(WinCountPlayer2)

    pygame.draw.rect(screen, PlayerColor, Player1)
    pygame.draw.rect(screen, PlayerColor, Player1)

    
    pygame.display.flip()

    
    clock.tick(60)

pygame.quit()
quit()






