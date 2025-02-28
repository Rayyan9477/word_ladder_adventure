import sys
from game.game_logic import WordLadderGame
from ui.main_screen import main_screen
from utils.dictionary_loader import DictionaryLoader
import logging

def main():
    # Setup logging configuration
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Display startup message
    logging.info("Starting Word Ladder Adventure Game...")
    
    # Load the word dictionary
    dictionary_loader = DictionaryLoader('data/dictionary.txt')
    words = dictionary_loader.get_all_words()
    logging.info(f"Dictionary loaded with {len(words)} words")
    
    # Initialize the main game screen
    main_screen()
    
    logging.info("Game session ended")


if __name__ == "__main__":
    main()