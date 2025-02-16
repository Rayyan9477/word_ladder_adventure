from algorithms.ucs import uniform_cost_search
from algorithms.a_star import a_star_search
from algorithms.bfs import breadth_first_search
from algorithms.gbfs import greedy_best_first_search

class HintSystem:
    def __init__(self, algorithm='ucs'):
        self.algorithm = algorithm

    def generate_hint(self, start_word, end_word, word_list):
        if self.algorithm == 'ucs':
            return uniform_cost_search(start_word, end_word, word_list)
        elif self.algorithm == 'a_star':
            return a_star_search(start_word, end_word, word_list)
        elif self.algorithm == 'bfs':
            return breadth_first_search(start_word, end_word, word_list)
        elif self.algorithm == 'gbfs':
            return greedy_best_first_search(start_word, end_word, word_list)
        else:
            raise ValueError("Invalid algorithm selected")

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm