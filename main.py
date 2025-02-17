import sys
from game.game_logic import WordLadderGame
from ui.main_screen import main_screen
from utils.dictionary_loader import DictionaryLoader
import logging

def main():

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Load the word dictionary
    dictionary_loader = DictionaryLoader('data/dictionary.txt')
    
    # Initialize the main game screen
    main_screen()


if __name__ == "__main__":
    main()