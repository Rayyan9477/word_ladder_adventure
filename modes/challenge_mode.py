from game.game_logic import WordLadderGame
from utils.dictionary_loader import DictionaryLoader

import logging

class ChallengeMode:
    def __init__(self):
        self.game_logic = WordLadderGame()
        self.dictionary = DictionaryLoader()
        self.max_attempts = 5  # Maximum attempts allowed
        self.current_attempts = 0
        self.max_hints =1
        self.setup_mode()

    def start_game(self):
        logging.info("Welcome to Challenge Mode!")
        logging.info("You have a maximum of {} attempts to complete the word ladder.".format(self.max_attempts))
        self.play_game()

    def play_game(self):
        while self.current_attempts < self.max_attempts:
            start_word = input("Enter the starting word: ")
            end_word = input("Enter the ending word: ")

            if not self.is_valid_word(start_word) or not self.is_valid_word(end_word):
                logging.warning("Invalid words. Please try again.")
                continue

            result = self.game_logic.find_word_ladder(start_word, end_word)

            if result:
                logging.info("Congratulations! You found a word ladder: ", result)
                break
            else:
                self.current_attempts += 1
                logging.warning("No valid word ladder found. Attempts left: {}".format(self.max_attempts - self.current_attempts))

        if self.current_attempts == self.max_attempts:
            logging.info("Game Over! You've used all your attempts.")

    def is_valid_word(self, word):
        return word in self.dictionary
    
    def setup_mode(self):
        """Configure game for challenge mode"""
        self.game.hints_remaining = self.max_hints
        self.game.max_moves -= 2  # Fewer moves
        
    def calculate_score(self):
        """Modified scoring for challenge mode"""
        base_score = self.game.calculate_score()
        return int(base_score * 1.5)  