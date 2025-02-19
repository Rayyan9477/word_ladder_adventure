from game.game_logic import WordLadderGame
from game.scoring import ScoringSystem
from utils.dictionary_loader import DictionaryLoader

import logging

class BeginnerMode:
    def __init__(self, game):
        self.game = game
        self.game_logic = WordLadderGame()
        self.scoring = ScoringSystem()
        self.word_dictionary = DictionaryLoader()
        self.max_attempts = 5  # Limit attempts for beginners
        self.current_attempts = 0
        self.max_hints = 5
        self.setup_mode()

    def start_game(self):
        logging.info("Welcome to the Beginner Mode of Word Ladder Adventure!")
        logging.info("You have a maximum of {} attempts to find the word ladder.".format(self.max_attempts))
        self.play_game()

    def play_game(self):
        while self.current_attempts < self.max_attempts:
            word = input("Enter a word: ")
            if self.validate_word(word):
                self.current_attempts += 1
                # Process the word and update game state
                self.game_logic.process_word(word)
                score = self.scoring.calculate_score(word)
                logging.info("Current Score: {}".format(score))
                if self.game_logic.check_win_condition():
                    logging.info("Congratulations! You've found the word ladder!")
                    break
            else:
                logging.warning("Invalid word. Please try again.")
        else:
            logging.info("Game Over! You've used all your attempts.")

    def validate_word(self, word):
        return word in self.word_dictionary
    

    def setup_mode(self):
        """Configure game for beginner mode"""
        self.game.hints_remaining = self.max_hints
        self.game.max_moves += 5  # Extra moves
        
    def calculate_score(self):
        """Modified scoring for beginners"""
        base_score = self.game.calculate_score()
        return int(base_score * 0.8)  # Reduced scoring pressure