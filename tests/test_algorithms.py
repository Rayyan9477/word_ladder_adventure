import unittest
from algorithms.ucs import uniform_cost_search
from algorithms.a_star import a_star_search
from algorithms.bfs import breadth_first_search
from algorithms.gbfs import greedy_best_first_search

class TestAlgorithms(unittest.TestCase):

    def setUp(self):
        self.start_word = "cold"
        self.end_word = "warm"
        self.word_list = ["cold", "cord", "card", "ward", "warm"]

    def test_uniform_cost_search(self):
        result = uniform_cost_search(self.start_word, self.end_word, self.word_list)
        expected_path = ["cold", "cord", "card", "ward", "warm"]
        self.assertEqual(result, expected_path)

    def test_a_star_search(self):
        result = a_star_search(self.start_word, self.end_word, self.word_list)
        expected_path = ["cold", "cord", "card", "ward", "warm"]
        self.assertEqual(result, expected_path)

    def test_breadth_first_search(self):
        result = breadth_first_search(self.start_word, self.end_word, self.word_list)
        expected_path = ["cold", "cord", "card", "ward", "warm"]
        self.assertEqual(result, expected_path)

    def test_greedy_best_first_search(self):
        result = greedy_best_first_search(self.start_word, self.end_word, self.word_list)
        expected_path = ["cold", "cord", "card", "ward", "warm"]
        self.assertEqual(result, expected_path)

if __name__ == '__main__':
    unittest.main()