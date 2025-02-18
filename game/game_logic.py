from algorithms.a_star import a_star_search
from algorithms.bfs import bfs
from algorithms.ucs import uniform_cost_search
from game.word_validator import is_valid_word
import logging

class WordLadderGame:
    def __init__(self, dictionary, algorithm='bfs', max_moves=20):
        """Initialize the game with dictionary and settings"""
        self.dictionary = {word.upper() for word in dictionary}
        self.algorithm = algorithm
        self.max_moves = max_moves
        # Initialize game state variables
        self.start_word = None
        self.end_word = None
        self.current_word = None
        self.solution_path = None
        self.player_path = None
        self.moves_remaining = max_moves
        self.hints_remaining = 3
        self.game_over = False  # Add this line
        self.won = False 
        
    def find_path(self, start_word, target_word):
        """Find path using selected algorithm"""
        if self.algorithm == 'bfs':
            return bfs(start_word, target_word, self.dictionary)
        elif self.algorithm == 'a_star':
            return a_star_search(start_word, target_word, self.dictionary)
        elif self.algorithm == 'ucs':
            return uniform_cost_search(start_word, target_word, self.dictionary)
        return None

    def start_game(self, start_word, end_word):
        """Initialize game with start and end words"""
        start_word = start_word.upper()
        end_word = end_word.upper()

        if not is_valid_word(start_word, self.dictionary) or not is_valid_word(end_word, self.dictionary):
            raise ValueError("Both words must be valid dictionary words")

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
        """Make a move in the game"""
        new_word = new_word.upper()
        
        if self.game_over:
            return False, "Game is already over"
            
        if self.moves_remaining <= 0:
            self.game_over = True
            return False, "No moves remaining"

        if new_word not in self.dictionary:
            return False, "Not a valid word"

        # Check if only one letter is different
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
        """Get AI hint for next move"""
        if self.hints_remaining <= 0:
            return None, "No hints remaining"
            
        if self.game_over:
            return None, "Game is over"
            
        current_index = len(self.player_path) - 1
        if current_index < len(self.solution_path) - 1:
            self.hints_remaining -= 1
            next_word = self.solution_path[current_index + 1]
            return next_word, f"Try: {next_word} ({self.hints_remaining} hints remaining)"
            
        return None, "No hint available"

    def get_graph_data(self):
        """Get data for graph visualization"""
        nodes = self.player_path.copy()
        edges = [(self.player_path[i], self.player_path[i+1]) 
                for i in range(len(self.player_path)-1)]
        return {
            'nodes': nodes,
            'edges': edges,
            'solution_path': self.solution_path
        }

    def reset_game(self):
        """Reset the game state to initial values"""
        self.start_word = None
        self.end_word = None
        self.current_word = None
        self.solution_path = None
        self.player_path = None
        self.moves_remaining = self.max_moves
        self.game_over = False  # Make sure this is included
        self.won = False       # Make sure this is included
        self.hints_remaining = 3