import sys
from game.game_logic import WordLadderGame
from ui.main_screen import main_screen
from utils.dictionary_loader import DictionaryLoader
import logging

def main():

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Load the word dictionary
    dictionary_loader = DictionaryLoader('data/dictionary.txt')
    word_dictionary = dictionary_loader.get_all_words()
    
    # Initialize the main game screen
    main_screen()

    # Start the game
    start_word = "start"  # Replace with the actual start word
    end_word = "end"      # Replace with the actual end word
    game = WordLadderGame(word_dictionary)
    game.start_game(start_word, end_word)

if __name__ == "__main__":
    main()