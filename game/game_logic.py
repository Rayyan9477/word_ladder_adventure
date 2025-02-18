import logging
from algorithms.a_star import a_star_search
from algorithms.bfs import bfs
from algorithms.ucs import uniform_cost_search
from game.word_validator import is_valid_word, is_one_letter_diff
import streamlit as st

class WordLadderGame:
    """
    Implements the core game logic for the Word Ladder game.
    """
    def __init__(self, dictionary, algorithm='a_star', max_moves=20):
        """
        Initializes the WordLadderGame.

        Args:
            dictionary (set): A set of valid words.
            algorithm (str): The search algorithm to use ('a_star', 'bfs', 'ucs').
            max_moves (int): The maximum number of moves allowed.
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
        logging.info(f"Game initialized with algorithm: {algorithm}, max_moves: {max_moves}")

    def start_game(self, start_word, end_word):
        """Start the game with the given start and end words."""
        start_word = start_word.upper()
        end_word = end_word.upper()
    
        if not is_valid_word(start_word, self.dictionary) or not is_valid_word(end_word, self.dictionary):
            raise ValueError("Both start and end words must be valid dictionary words.")
    
        # Check if words are the same length
        if len(start_word) != len(end_word):
            raise ValueError("Start and end words must be the same length.")
    
        self.start_word = start_word
        self.end_word = end_word
        self.current_word = start_word
        self.score = 0
        self.moves_remaining = self.max_moves
    
        # Try all algorithms in order of efficiency
        word_ladder = None
        
        if self.algorithm == 'bfs':
            word_ladder = bfs(start_word, end_word, self.dictionary)
        elif self.algorithm == 'a_star':
            word_ladder = a_star_search(start_word, end_word, self.dictionary)
        elif self.algorithm == 'ucs':
            word_ladder = uniform_cost_search(start_word, end_word, self.dictionary)
    
        if not word_ladder:
            # If the chosen algorithm fails, try others
            algorithms = ['bfs', 'a_star', 'ucs']
            for alg in algorithms:
                if alg != self.algorithm:
                    if alg == 'bfs':
                        word_ladder = bfs(start_word, end_word, self.dictionary)
                    elif alg == 'a_star':
                        word_ladder = a_star_search(start_word, end_word, self.dictionary)
                    elif alg == 'ucs':
                        word_ladder = uniform_cost_search(start_word, end_word, self.dictionary)
                    if word_ladder:
                        break
    
        if not word_ladder:
            # If no path is found, suggest intermediate words
            intermediate_words = self.find_intermediate_words(start_word, end_word)
            if intermediate_words:
                suggestion = f"Try using these intermediate words: {' -> '.join(intermediate_words)}"
            else:
                similar_words = self.find_similar_words(end_word)
                suggestion = f"Try these similar words instead: {', '.join(similar_words[:3])}" if similar_words else ""
            raise ValueError(f"No direct word ladder found from {start_word} to {end_word}. {suggestion}")
    
        self.word_ladder = word_ladder
        logging.info(f"Game started! Transform '{self.start_word}' to '{self.end_word}'.")
        logging.info(f"Word ladder found: {self.word_ladder}")
    
    def find_intermediate_words(self, start_word, end_word):
        """Find possible intermediate words that could help form a path."""
        intermediate = []
        # Find words that share letters with both start and end words
        for word in self.dictionary:
            if len(word) == len(start_word):
                start_diff = sum(1 for a, b in zip(word, start_word) if a != b)
                end_diff = sum(1 for a, b in zip(word, end_word) if a != b)
                if start_diff <= 2 and end_diff <= 2:
                    intermediate.append(word)
        return sorted(intermediate, key=lambda w: (
            sum(1 for a, b in zip(w, start_word) if a != b) +
            sum(1 for a, b in zip(w, end_word) if a != b)
        ))[:3]
    
    def find_similar_words(self, word):
        """Find words that are similar to the given word."""
        similar = []
        for dict_word in self.dictionary:
            if len(dict_word) == len(word):
                diff_count = sum(1 for a, b in zip(word, dict_word) if a != b)
                if diff_count == 1:
                    similar.append(dict_word)
        return similar

    def make_move(self, new_word):
        """
        Makes a move by transforming the current word to the new word.

        Args:
            new_word (str): The word to move to.

        Returns:
            bool: True if the move is successful, False otherwise.
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
        Checks if the new word is a valid transformation of the current word.

        Args:
            new_word (str): The word to check.

        Returns:
            bool: True if the transformation is valid, False otherwise.
        """
        if new_word not in self.dictionary:
            return False
        return self.is_one_letter_different(self.current_word, new_word)

    @staticmethod
    def is_one_letter_different(word1, word2):
        """
        Checks if two words differ by exactly one letter.

        Args:
            word1 (str): The first word.
            word2 (str): The second word.

        Returns:
            bool: True if the words differ by one letter, False otherwise.
        """
        if len(word1) != len(word2):
            return False
        difference_count = sum(1 for a, b in zip(word1, word2) if a != b)
        return difference_count == 1

    def get_score(self):
        """
        Gets the current score of the game.

        Returns:
            int: The current score.
        """
        return self.score

    def get_word_ladder(self):
        """
        Gets the current word ladder.

        Returns:
            list: The current word ladder.
        """
        return self.word_ladder

    def get_moves_remaining(self):
        """
        Gets the number of moves remaining.

        Returns:
            int: The number of moves remaining.
        """
        return self.moves_remaining

    def reset_game(self):
        """
        Resets the game to its initial state.
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
        Provides a hint to the player.

        Returns:
            str: The next word in the ladder, or None if no hint is available.
        """
        if self.word_ladder and len(self.word_ladder) > 1:
            return self.word_ladder[1]  # Return the next word in the ladder
        else:
            return None