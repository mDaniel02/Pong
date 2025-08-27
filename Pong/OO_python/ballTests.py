import unittest
import pygame
import time
from player import Ball 



class TestBall(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global screen
        global WindowWidth
        global WindowHeight

        #os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()

        WindowWidth = 1920
        WindowHeight = 1080
        screen = pygame.display.set_mode((WindowWidth, WindowHeight))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.ball = Ball(100, 100, 10, 7, (255, 255, 255))

    def test_initial_position(self):
        self.assertEqual(self.ball.posx, 100)
        self.assertEqual(self.ball.posy, 100)

    def test_update_movement(self):
        old_x, old_y = self.ball.posx, self.ball.posy
        self.ball.update()
        self.assertEqual(self.ball.posx, old_x + self.ball.speed * self.ball.xFac)
        self.assertEqual(self.ball.posy, old_y + self.ball.speed * self.ball.yFac)

    def test_vertical_bounce(self):
        self.ball.posy = 5
        old_yFac = self.ball.yFac
        self.ball.update()
        self.assertEqual(self.ball.yFac, -old_yFac)

    def test_score_right_player(self):
        self.ball.posx = 0 
        result = self.ball.update()
        self.assertEqual(result, 0)

    def test_score_left_player(self):
        self.ball.posx = WindowWidth 
        result = self.ball.update()
        self.assertEqual(result, -1)

    def test_hit(self):
        old_xFac = self.ball.xFac
        self.ball.hit()
        self.assertEqual(self.ball.xFac, -old_xFac)

    def test_reset(self):
        self.ball.posx = WindowWidth // 2
        self.ball.posy = WindowHeight // 2
        self.ball.firstTime = 0

        start_time = time.time()
        self.ball.reset()
        end_time = time.time()

        self.assertEqual(self.ball.posx, WindowWidth // 2)
        self.assertEqual(self.ball.posy, WindowHeight // 2)
        self.assertEqual(self.ball.firstTime, 1)
        self.assertGreaterEqual(end_time - start_time, 0.5)
    
    def test_get_rect(self):
        rect = self.ball.getRect()
        self.assertEqual(rect.width, self.ball.radius * 2)
        self.assertEqual(rect.height, self.ball.radius * 2)
        self.assertEqual(rect.center, (self.ball.posx, self.ball.posy))

    def test_vertical_bounce_top(self):
        self.ball.yFac = -1  
        self.ball.posy = self.ball.radius  

        self.ball.update()

        self.assertEqual(self.ball.yFac, 1) 

    def test_vertical_bounce_bottom(self):
        self.ball.yFac = 1  
        self.ball.posy = WindowHeight - self.ball.radius  

        self.ball.update()

        self.assertEqual(self.ball.yFac, -1)



if __name__ == '__main__':
    unittest.main()