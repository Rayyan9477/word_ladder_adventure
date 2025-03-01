import sys
from game.game_logic import WordLadderGame
from ui.main_screen import main_screen
from utils.dictionary_loader import DictionaryLoader
import logging

def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    logging.info("Starting Word Ladder Adventure Game...")
    
    dictionary_loader = DictionaryLoader('data/dictionary.txt')
    words = dictionary_loader.get_all_words()
    logging.info(f"Dictionary loaded with {len(words)} words")
    
    main_screen()
    
    logging.info("Game session ended")


if __name__ == "__main__":
    main()