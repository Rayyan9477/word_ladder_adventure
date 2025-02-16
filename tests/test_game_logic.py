import unittest
from game.game_logic import WordLadderGame
from utils.dictionary_loader import DictionaryLoader

class TestGameLogic(unittest.TestCase):

    def setUp(self):
        dictionary_loader = DictionaryLoader('data/dictionary.txt')
        word_dictionary = dictionary_loader.get_all_words()
        self.game = WordLadderGame(word_dictionary)

    def test_start_game(self):
        self.game.start_game("cat", "bat")
        self.assertEqual(self.game.start_word, "cat")
        self.assertEqual(self.game.end_word, "bat")
        self.assertTrue(self.game.is_valid_transformation("bat"))

    def test_valid_word_transformation(self):
        self.game.start_game("cat", "bat")
        self.assertTrue(self.game.is_valid_transformation("bat"))

    def test_invalid_word_transformation(self):
        self.game.start_game("cat", "bat")
        self.assertFalse(self.game.is_valid_transformation("dog"))

    def test_win_condition(self):
        self.game.start_game("cat", "bat")
        self.game.make_move("bat")
        self.assertEqual(self.game.current_word, "bat")
        self.assertTrue(self.game.make_move("bat"))

    def test_score_update(self):
        self.game.start_game("cat", "bat")
        initial_score = self.game.get_score()
        self.game.make_move("bat")
        self.assertGreater(self.game.get_score(), initial_score)

if __name__ == '__main__':
    unittest.main()