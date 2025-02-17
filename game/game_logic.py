import logging
from algorithms.a_star import a_star_search
from algorithms.bfs import bfs
from algorithms.ucs import uniform_cost_search
from game.word_validator import is_valid_word, is_one_letter_diff

class WordLadderGame:
    def __init__(self, dictionary, algorithm='a_star', max_moves=20):
        """
        Initialize the Word Ladder Game with a given dictionary and algorithm.
        """
        self.dictionary = dictionary
        self.start_word = None
        self.end_word = None
        self.current_word = None
        self.score = 0
        self.word_ladder = []
        self.algorithm = algorithm
        self.max_moves = max_moves
        self.moves_remaining = max_moves

    def start_game(self, start_word, end_word):
        """
        Start the game with the given start and end words.
        """
        if not is_valid_word(start_word, self.dictionary) or not is_valid_word(end_word, self.dictionary):
            raise ValueError("Both start and end words must be valid dictionary words.")

        if not is_one_letter_diff(start_word, end_word) and self.algorithm == 'a_star':
            logging.warning("A* search is best suited for words that are one letter apart.")

        self.start_word = start_word
        self.end_word = end_word
        self.current_word = start_word
        self.score = 0
        self.moves_remaining = self.max_moves

        # Use the selected algorithm to find the word ladder
        if self.algorithm == 'a_star':
            self.word_ladder = a_star_search(start_word, end_word, self.dictionary)
        elif self.algorithm == 'bfs':
            self.word_ladder = bfs(start_word, end_word, self.dictionary)
        elif self.algorithm == 'ucs':
            self.word_ladder = uniform_cost_search(start_word, end_word, self.dictionary)
        else:
            raise ValueError("Invalid algorithm selected.")

        if not self.word_ladder:
            raise ValueError("No word ladder found for the given words.")

        logging.info(f"Game started! Transform '{self.start_word}' to '{self.end_word}'.")
        logging.info(f"Word ladder: {self.word_ladder}")

    def make_move(self, new_word):
        """
        Make a move by transforming the current word to the new word.
        """
        if self.moves_remaining <= 0:
            logging.info("No moves remaining. Game Over!")
            return False

        if not self.word_ladder or len(self.word_ladder) <= 1:
            logging.info("Word ladder is empty or complete.")
            return False

        if len(self.word_ladder) > 1:
            next_word = self.word_ladder[1]
        else:
            next_word = self.end_word

        if new_word == next_word:
            self.word_ladder.pop(0)
            self.current_word = new_word
            self.score += 1
            self.moves_remaining -= 1
            logging.info(f"Moved to '{new_word}'. Current score: {self.score}, Moves remaining: {self.moves_remaining}.")
            if new_word == self.end_word:
                logging.info("Congratulations! You've completed the word ladder!")
                return True
        else:
            logging.warning(f"'{new_word}' is not a valid transformation. Expected '{next_word}'.")
        return False

    def is_valid_transformation(self, new_word):
        """
        Check if the new word is a valid transformation of the current word.
        """
        if new_word not in self.dictionary:
            return False
        return self.is_one_letter_different(self.current_word, new_word)

    @staticmethod
    def is_one_letter_different(word1, word2):
        """
        Check if two words differ by exactly one letter.
        """
        if len(word1) != len(word2):
            return False
        difference_count = sum(1 for a, b in zip(word1, word2) if a != b)
        return difference_count == 1

    def get_score(self):
        """
        Get the current score of the game.
        """
        return self.score

    def get_word_ladder(self):
        """
        Get the current word ladder.
        """
        return self.word_ladder

    def get_moves_remaining(self):
        """
        Get the number of moves remaining.
        """
        return self.moves_remaining

    def reset_game(self):
        """
        Reset the game to its initial state.
        """
        self.start_word = None
        self.end_word = None
        self.current_word = None
        self.score = 0
        self.word_ladder = []
        self.moves_remaining = self.max_moves
        logging.info("Game has been reset.")

    def get_hint(self):
        """
        Provide a hint to the player.
        """
        if self.word_ladder and len(self.word_ladder) > 1:
            return self.word_ladder[1]  # Return the next word in the ladder
        else:
            return None