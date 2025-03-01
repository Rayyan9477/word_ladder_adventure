from algorithms.a_star import a_star_search
from algorithms.bfs import bfs
from algorithms.ucs import uniform_cost_search
from algorithms.gbfs import greedy_best_first_search
from game.word_validator import is_valid_word
from ai.hint_system import HintSystem
import logging
import time

class WordLadderGame:
    def __init__(self, dictionary, algorithm='bfs', max_moves=20, mode="Normal"):
        self.dictionary = {word.upper() for word in dictionary}
        self.algorithm = algorithm.lower()
        self.max_moves = max_moves
        self.mode = mode
        self.start_word = None
        self.end_word = None
        self.current_word = None
        self.solution_path = None
        self.player_path = None
        self.moves_remaining = max_moves
        
        if mode == "Beginner":
            self.hints_remaining = 5
        elif mode == "Challenge":
            self.hints_remaining = 1
        else:
            self.hints_remaining = 3
            
        self.game_over = False
        self.won = False
        self.hint_system = HintSystem(self.dictionary)
        self.algorithm_stats = {}
        
    def find_path(self, start_word, target_word):
        algorithms = {
            'bfs': bfs,
            'a_star': a_star_search,
            'a*': a_star_search,
            'ucs': uniform_cost_search,
            'gbfs': lambda s, t, d: greedy_best_first_search(s, t, d)
        }
        
        if self.algorithm not in algorithms:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")
        
        start_time = time.time()
        try:
            path = algorithms[self.algorithm](start_word, target_word, self.dictionary)
            end_time = time.time()
            
            self.algorithm_stats = {
                'name': self.algorithm,
                'time_taken': end_time - start_time,
                'path_length': len(path) - 1 if path else None,
                'path': path
            }
        except Exception as e:
            logging.error(f"Error running algorithm {self.algorithm}: {str(e)}")
            path = None
            self.algorithm_stats = {
                'name': self.algorithm,
                'time_taken': 0,
                'path_length': None,
                'path': None
            }
            
        return path
        
    def compare_algorithms(self, start_word, target_word):
        algorithms = {
            'bfs': bfs,
            'a_star': a_star_search,
            'ucs': uniform_cost_search,
            'gbfs': lambda s, t, d: greedy_best_first_search(s, t, d)
        }
        
        results = {}
        for name, algorithm in algorithms.items():
            start_time = time.time()
            try:
                path = algorithm(start_word, target_word, self.dictionary)
                end_time = time.time()
                
                results[name] = {
                    'time_taken': end_time - start_time,
                    'path_length': len(path) - 1 if path else None,
                    'path': path
                }
            except Exception as e:
                logging.error(f"Error running algorithm {name}: {str(e)}")
                results[name] = {
                    'time_taken': 0,
                    'path_length': None,
                    'path': None
                }
            
        return results

    def start_game(self, start_word, end_word):
        start_word = start_word.upper()
        end_word = end_word.upper()

        if len(start_word) != len(end_word):
            raise ValueError("Start and end words must have the same length")

        if not is_valid_word(start_word, self.dictionary) or not is_valid_word(end_word, self.dictionary):
            raise ValueError("Both words must be valid dictionary words")

        self.algorithm_comparisons = self.compare_algorithms(start_word, end_word)
        
        self.solution_path = self.find_path(start_word, end_word)
        if not self.solution_path:
            raise ValueError("No valid path exists between these words")

        self.start_word = start_word
        self.end_word = end_word
        self.current_word = start_word
        self.player_path = [start_word]
        self.moves_remaining = self.max_moves
        self.game_over = False
        self.won = False
        
        return True

    def make_move(self, new_word):
        new_word = new_word.upper()
        
        if self.game_over:
            return False, "Game is already over"
            
        if self.moves_remaining <= 0:
            self.game_over = True
            return False, "No moves remaining"

        if new_word not in self.dictionary:
            return False, "Not a valid word"

        if len(new_word) != len(self.current_word):
            return False, "Words must be the same length"
            
        diff_count = sum(1 for a, b in zip(self.current_word, new_word) if a != b)
        if diff_count != 1:
            return False, "Must change exactly one letter"

        self.moves_remaining -= 1
        self.current_word = new_word
        self.player_path.append(new_word)

        if new_word == self.end_word:
            self.game_over = True
            self.won = True
            return True, "Congratulations! You've reached the target word!"

        if self.moves_remaining == 0:
            self.game_over = True
            return False, "Game Over - No moves remaining"

        return True, f"Valid move! {self.moves_remaining} moves remaining"

    def get_hint(self):
        if self.hints_remaining <= 0:
            return None, "No hints remaining"
        
        if self.game_over:
            return None, "Game is over"
            
        next_word = self.hint_system.get_next_move(
            self.current_word, 
            self.end_word, 
            self.solution_path
        )
        
        if next_word:
            self.hints_remaining -= 1
            difficulty = self.hint_system.get_difficulty_hint(
                (self.current_word, next_word)
            )
            return next_word, f"Try: {next_word} (Difficulty: {difficulty}, {self.hints_remaining} hints remaining)"
        
        return None, "No hint available"

    def get_graph_data(self, key=None):
        data = {
            'nodes': self.player_path.copy() if self.player_path else [],
            'edges': [(self.player_path[i], self.player_path[i+1]) 
                    for i in range(len(self.player_path)-1)] if self.player_path and len(self.player_path) > 1 else [],
            'solution_path': self.solution_path if self.solution_path else []
        }
        
        if key and key in data:
            return data[key]
            
        return data
        
    def get_algorithm_comparison(self):
        if not hasattr(self, 'algorithm_comparisons'):
            return None
            
        return self.algorithm_comparisons

    def reset_game(self):
        self.start_word = None
        self.end_word = None
        self.current_word = None
        self.solution_path = None
        self.player_path = None
        self.moves_remaining = self.max_moves
        self.game_over = False
        self.won = False
        
        if self.mode == "Beginner":
            self.hints_remaining = 5
        elif self.mode == "Challenge":
            self.hints_remaining = 1
        else:
            self.hints_remaining = 3

    def calculate_score(self):
        base_score = 100
        move_penalty = 5 * max(0, len(self.player_path) - len(self.solution_path))
        
        if self.mode == "Beginner":
            max_hints = 5
            hint_penalty = 5 * (max_hints - self.hints_remaining)
        elif self.mode == "Challenge":
            max_hints = 1
            hint_penalty = 20 * (max_hints - self.hints_remaining)
        else:
            max_hints = 3
            hint_penalty = 10 * (max_hints - self.hints_remaining)
            
        return max(0, base_score - move_penalty - hint_penalty)