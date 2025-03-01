from algorithms.ucs import uniform_cost_search
from algorithms.a_star import a_star_search
from algorithms.gbfs import greedy_best_first_search
from algorithms.gbfs import greedy_best_first_search, get_neighbors

from algorithms.bfs import bfs
import random

class HintSystem:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        
    def get_next_move(self, current_word, target_word, solution_path=None):
        if solution_path:
            try:
                current_index = solution_path.index(current_word)
                if current_index < len(solution_path) - 1:
                    return solution_path[current_index + 1]
            except ValueError:
                pass
        
        new_path = bfs(current_word, target_word, self.dictionary)
        if new_path and len(new_path) > 1:
            return new_path[1]  
        
        return self.get_any_valid_move(current_word)
            
    def get_any_valid_move(self, word):
        for i in range(len(word)):
            for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if c == word[i]:
                    continue
                    
                new_word = word[:i] + c + word[i+1:]
                if new_word in self.dictionary:
                    return new_word
        
        return None
        
    def get_difficulty_hint(self, word_pair):
        if not word_pair or len(word_pair) != 2:
            return "Unknown"
            
        current_word, next_word = word_pair
        
        diff_positions = [i for i, (a, b) in enumerate(zip(current_word, next_word)) if a != b]
        if not diff_positions:
            return "Easy"
            
        position = diff_positions[0]
        
        if position == 0 or position == len(current_word) - 1:
            return "Easy"
            
        common_letters = 'AEIOURSTLN'
        if next_word[position] in common_letters:
            return "Medium"
            
        return "Hard"