import unittest
from unittest.mock import patch, MagicMock
from player import WinCondition

WHITE = (255, 255, 255)
WindowWidth = 1920
WindowHeight = 1080

class TestWinCondition(unittest.TestCase):
    
    @patch("pygame.font.Font")
    def setUp(self, mock_font):

        mock_font.return_value.render.return_value = MagicMock()
        self.win_condition = WinCondition(max_score=5)

    def test_initial_state(self):
        self.assertIsNone(self.win_condition.winner)
        self.assertEqual(self.win_condition.max_score, 5)
        self.assertEqual(self.win_condition.winner_display_time, 180)

    def test_check_player1_wins(self):
        result = self.win_condition.check(p1_score=5, p2_score=3)
        self.assertEqual(result, (True, "Player 1 wins"))
        self.assertEqual(self.win_condition.winner, "Player 1 wins")

    def test_check_player2_wins(self):
        result = self.win_condition.check(p1_score=2, p2_score=5)
        self.assertEqual(result, (True, "Player 2 wins"))
        self.assertEqual(self.win_condition.winner, "Player 2 wins")

    def test_check_no_winner(self):
        result = self.win_condition.check(p1_score=3, p2_score=4)
        self.assertFalse(result)

    def test_check_winner_method_matches_check(self):
        self.win_condition.reset()
        result = self.win_condition.check_winner(p1_score=5, p2_score=0)
        self.assertEqual(result, (True, "Player 1 wins"))

        self.win_condition.reset()
        result = self.win_condition.check_winner(p1_score=0, p2_score=5)
        self.assertEqual(result, (True, "Player 2 wins"))

        self.win_condition.reset()
        result = self.win_condition.check_winner(p1_score=3, p2_score=3)
        self.assertEqual(result, (False, ""))

    def test_reset_functionality(self):
        self.win_condition.winner = "Player 1 wins"
        self.win_condition.winner_display_time = 100
        self.win_condition.reset()
        self.assertIsNone(self.win_condition.winner)
        self.assertEqual(self.win_condition.winner_display_time, 180)

    
    @patch("pygame.font.Font")
    def test_draw_winner_skips_if_no_winner(self, mock_font):
        mock_screen = MagicMock()
        self.win_condition.winner = None
        self.win_condition.draw_winner(mock_screen)
        mock_screen.blit.assert_not_called()


if __name__ == "__main__":
    unittest.main()