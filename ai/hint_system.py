from algorithms.ucs import uniform_cost_search
from algorithms.a_star import a_star_search
from algorithms.bfs import breadth_first_search
from algorithms.gbfs import greedy_best_first_search


class HintSystem:
    def __init__(self, algorithm='bfs', dictionary=None):
        self.algorithm = algorithm
        self.dictionary = dictionary or set()

    def get_next_move(self, current_word, target_word, solution_path):
        """Get optimal next move from solution path"""
        if not solution_path:
            return self.generate_hint(current_word, target_word)
            
        try:
            current_index = solution_path.index(current_word)
            if current_index < len(solution_path) - 1:
                return solution_path[current_index + 1]
        except ValueError:
            return self.generate_hint(current_word, target_word)
        
        return None

    def generate_hint(self, start_word, target_word):
        """Generate a new hint using the selected algorithm"""
        from algorithms.algorithm_factory import create_algorithm
        
        algorithm = create_algorithm(self.algorithm)
        path = algorithm.find_path(start_word, target_word, self.dictionary)
        
        if path and len(path) > 1:
            return path[1]  # Return first step after current word
        return None

    def get_difficulty_hint(self, word_pair):
        """Estimate transformation difficulty"""
        start_word, end_word = word_pair
        diff_count = sum(1 for a, b in zip(start_word, end_word) if a != b)
        
        if diff_count <= 2:
            return "Easy"
        elif diff_count <= 4:
            return "Medium"
        return "Hard"