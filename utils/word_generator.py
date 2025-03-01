import random
from algorithms.bfs import bfs  
from algorithms.gbfs import greedy_best_first_search
from algorithms.a_star import a_star_search
from algorithms.ucs import uniform_cost_search
import time

class RandomWordGenerator:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.word_lengths = {3: [], 4: [], 5: [], 6: [], 7: []}
        self._categorize_words()
        
    def _categorize_words(self):
        """Categorize words by length for faster retrieval"""
        for word in self.dictionary:
            length = len(word)
            if 3 <= length <= 7:  
                if word not in self.word_lengths[length]:
                    self.word_lengths[length].append(word)

    def get_random_pair(self, difficulty="medium"):
        
        if difficulty == "easy":
            lengths = [3, 4]
        elif difficulty == "medium":
            lengths = [5]
        else:  # hard
            lengths = [6, 7]
            
        length = random.choice(lengths)
        words = self.word_lengths[length]
        
        if len(words) < 2:
            return None, None
            
        for _ in range(20):  # Try 20 times (increased from 10)
            start_word = random.choice(words)
            end_word = random.choice(words)
            
            if start_word != end_word:
                path = bfs(start_word, end_word, self.dictionary)
                if path and 2 <= len(path) <= 10: 
                    return start_word, end_word
                
        common_words = self._get_most_connected_words(length)
        if common_words and len(common_words) >= 2:
            return random.choice(common_words), random.choice(common_words)
        
        return words[0], words[-1]
    
    def _get_most_connected_words(self, length):
        words = self.word_lengths[length][:100]  
        if not words:
            return []
            
        common_letters = 'ETAOINSRHL'
        common_words = [word for word in words 
                      if any(letter in word for letter in common_letters)]
        
        return common_words or words