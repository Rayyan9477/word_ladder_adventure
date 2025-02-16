from game.game_logic import GameLogic
from game.scoring import Scoring
from utils.dictionary_loader import load_dictionary

import logging

class BeginnerMode:
    def __init__(self):
        self.game_logic = GameLogic()
        self.scoring = Scoring()
        self.word_dictionary = load_dictionary()
        self.max_attempts = 5  # Limit attempts for beginners
        self.current_attempts = 0

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