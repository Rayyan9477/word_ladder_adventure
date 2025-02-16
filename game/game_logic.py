import logging

class WordLadderGame:
    def __init__(self, dictionary):
        """
        Initialize the Word Ladder Game with a given dictionary.
        """
        self.dictionary = dictionary
        self.start_word = None
        self.end_word = None
        self.current_word = None
        self.score = 0
        self.word_ladder = []

    def start_game(self, start_word, end_word):
        """
        Start the game with the given start and end words.
        """
        if start_word not in self.dictionary or end_word not in self.dictionary:
            raise ValueError("Both start and end words must be valid dictionary words.")
        self.start_word = start_word
        self.end_word = end_word
        self.current_word = start_word
        self.word_ladder = [start_word]
        self.score = 0
        logging.info(f"Game started! Transform '{self.start_word}' to '{self.end_word}'.")

    def make_move(self, new_word):
        """
        Make a move by transforming the current word to the new word.
        """
        if self.is_valid_transformation(new_word):
            self.current_word = new_word
            self.word_ladder.append(new_word)
            self.score += 1
            logging.info(f"Moved to '{new_word}'. Current score: {self.score}.")
            if new_word == self.end_word:
                logging.info("Congratulations! You've completed the word ladder!")
                return True
        else:
            logging.warning(f"'{new_word}' is not a valid transformation.")
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

    def reset_game(self):
        """
        Reset the game to its initial state.
        """
        self.start_word = None
        self.end_word = None
        self.current_word = None
        self.score = 0
        self.word_ladder = []
        logging.info("Game has been reset.")