from game.game_logic import GameLogic
from utils.dictionary_loader import load_dictionary

import logging

class ChallengeMode:
    def __init__(self):
        self.game_logic = GameLogic()
        self.dictionary = load_dictionary()
        self.max_attempts = 5  # Maximum attempts allowed
        self.current_attempts = 0

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