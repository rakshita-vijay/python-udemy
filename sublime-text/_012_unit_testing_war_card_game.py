import unittest
import _011_war_card_game

class TestWar(unittest.TestCase):
    def test_war(self):
        res = _011_war_card_game.game_of_war()
        self.assertEqual(res, 52)

if __name__ == "__main__":
    unittest.main()
