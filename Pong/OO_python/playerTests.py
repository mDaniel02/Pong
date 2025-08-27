import unittest
import pygame
from player import Players


class TestPlayer(unittest.TestCase):
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
        self.player = Players(50,100,20,100,5,(255,255,255))
    
    def test_intialisation(self):
        self.assertEqual(self.player.posx, 50)
        self.assertEqual(self.player.posy, 100)
        self.assertEqual(self.player.width, 20)
        self.assertEqual(self.player.height, 100)
        self.assertEqual(self.player.speed, 5)
        self.assertEqual(self.player.color, (255,255,255))
        self.assertIsInstance(self.player.getRect(), pygame.Rect)

    def test_update_movement_down(self):
        self.player.update(1)
        self.assertEqual(self.player.posy, 105)

    def test_updat_movement_up(self):
        self.player.update(-1)
        self.assertEqual(self.player.posy, 95)

    def test_update_top_boundary(self):
        self.player.posy = 0
        self.player.update(-1)
        self.assertEqual(self.player.posy, 0)

    def test_update_bottom_boundary(self):
        self.player.posy = 0
        self.player.update(1)
        self.assertEqual(self.player.posy, 5) 
    
    def test_get_set_state(self):
        self.assertEqual(self.player.get_state(), 100)
        self.player.set_state(300)
        self.assertEqual(self.player.posy, 300)
        self.assertEqual(self.player.posy, 300)
    
    def test_getRect_after_update(self):
        self.player.update(5)
        rect = self.player.getRect()
        self.assertEqual(rect.y, self.player.posy)

if __name__ == '__main__':
    unittest.main()

        