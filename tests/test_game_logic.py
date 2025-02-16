import unittest
from game.game_logic import Game
from game.word_validator import WordValidator

class TestGameLogic(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.validator = WordValidator()

    def test_start_game(self):
        self.game.start()
        self.assertTrue(self.game.is_running)

    def test_valid_word_transformation(self):
        valid_word = "cat"
        next_word = "bat"
        self.assertTrue(self.validator.is_valid_transformation(valid_word, next_word))

    def test_invalid_word_transformation(self):
        valid_word = "cat"
        next_word = "dog"
        self.assertFalse(self.validator.is_valid_transformation(valid_word, next_word))

    def test_win_condition(self):
        self.game.start()
        self.game.current_word = "cat"
        self.game.target_word = "bat"
        self.game.make_move("bat")
        self.assertTrue(self.game.check_win())

    def test_score_update(self):
        self.game.start()
        initial_score = self.game.score
        self.game.make_move("bat")
        self.assertGreater(self.game.score, initial_score)

    def test_invalid_move(self):
        self.game.start()
        self.game.current_word = "cat"
        with self.assertRaises(ValueError):
            self.game.make_move("dog")

if __name__ == '__main__':
    unittest.main()