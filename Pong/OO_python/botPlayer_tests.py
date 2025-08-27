import unittest
import pygame
from player import Ball, BotPlayer
WindowWidth = 1920
WindowHeight = 1080

pygame.init()
screen = pygame.Surface((WindowWidth, WindowHeight)) 



class TestBotPlayerWithBall(unittest.TestCase):
    def setUp(self):
        self.bot = BotPlayer(posx=350, posy=150, width=10, height=50, speed=5, color=(255, 255, 255))

    def test_bot_moves_towards_ball(self):
        ball = Ball(posx=100, posy=100, radius=5, speed=10, color=(255, 255, 255))
        ball.xFac = 1  

        initial_pos = self.bot.posy
        self.bot.auto_move(ball)
        self.assertNotEqual(self.bot.posy, initial_pos, "Bot should move towards the ball")

    def test_bot_does_not_move_when_ball_away(self):
        ball = Ball(posx=360, posy=100, radius=5, speed=10, color=(255, 255, 255))
        ball.xFac = -1  
        initial_pos = self.bot.posy
        self.bot.auto_move(ball)
        self.assertEqual(self.bot.posy, initial_pos, "Bot should not move when ball moving away")

    def test_bot_predicts_bounce_top(self):
        ball = Ball(posx=200, posy=0, radius=5, speed=10, color=(255, 255, 255))
        ball.xFac = 1
        ball.yFac = -1

        initial_pos = self.bot.posy
        self.bot.auto_move(ball)
        self.assertNotEqual(self.bot.posy, initial_pos, "Bot should move when ball predicted to bounce off top")

    def test_bot_predicts_bounce_bottom(self):
        ball = Ball(posx=200, posy=WindowHeight, radius=5, speed=10, color=(255, 255, 255))
        ball.xFac = 1
        ball.yFac = 1

        initial_pos = self.bot.posy
        self.bot.auto_move(ball)
        self.assertNotEqual(self.bot.posy, initial_pos, "Bot should move when ball predicted to bounce off bottom")

if __name__ == '__main__':
    unittest.main()

#python -m unittest -v botPlayer_tests