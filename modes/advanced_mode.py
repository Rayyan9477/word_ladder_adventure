from game.game_logic import GameLogic
from utils.dictionary_loader import load_dictionary

import logging

class AdvancedMode:
    def __init__(self):
        self.game_logic = GameLogic()
        self.dictionary = load_dictionary()
        self.max_attempts = 5
        self.current_attempts = 0

    def start_game(self):
        logging.info("Welcome to Advanced Mode!")
        logging.info("You have a maximum of {} attempts to complete the word ladder.".format(self.max_attempts))
        self.play_game()

    def play_game(self):
        while self.current_attempts < self.max_attempts:
            start_word = input("Enter the starting word: ")
            end_word = input("Enter the ending word: ")

            if self.validate_words(start_word, end_word):
                self.game_logic.play(start_word, end_word)
                break
            else:
                self.current_attempts += 1
                logging.warning("Invalid words or transformation. Attempts left: {}".format(self.max_attempts - self.current_attempts))

        if self.current_attempts == self.max_attempts:
            logging.info("Game Over! You've used all your attempts.")

    def validate_words(self, start_word, end_word):
        return start_word in self.dictionary and end_word in self.dictionary