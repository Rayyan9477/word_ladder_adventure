import unittest
from ai.hint_system import HintSystem
from ai.algorithm_selector import AlgorithmSelector

class TestAIComponents(unittest.TestCase):

    def setUp(self):
        self.hint_system = HintSystem()
        self.algorithm_selector = AlgorithmSelector()

    def test_hint_generation(self):
        # Test hint generation for a specific word ladder
        start_word = "cold"
        end_word = "warm"
        hint = self.hint_system.generate_hint(start_word, end_word)
        self.assertIsNotNone(hint)
        self.assertIn(hint, ["Use a word that changes one letter.", "Try a word that is similar in length."])

    def test_algorithm_selection(self):
        # Test algorithm selection functionality
        selected_algorithm = self.algorithm_selector.select_algorithm("A*")
        self.assertEqual(selected_algorithm, "A*")
        
        selected_algorithm = self.algorithm_selector.select_algorithm("BFS")
        self.assertEqual(selected_algorithm, "BFS")

    def test_invalid_algorithm_selection(self):
        # Test handling of invalid algorithm selection
        with self.assertRaises(ValueError):
            self.algorithm_selector.select_algorithm("InvalidAlgorithm")

if __name__ == '__main__':
    unittest.main()