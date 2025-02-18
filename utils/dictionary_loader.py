import logging
import os

class DictionaryLoader:
    def __init__(self, dictionary_file='data/dictionary.txt'):
        self.dictionary_file = dictionary_file
        self.words = self.load_dictionary()

    def load_dictionary(self):
        try:
            with open(self.dictionary_file, 'r') as file:
                # Store words in both uppercase and lowercase
                words = set()
                for line in file:
                    word = line.strip()
                    if word:  # Skip empty lines
                        words.add(word.upper())  # Add uppercase version
                        words.add(word.lower())  # Add lowercase version
                logging.info(f"Loaded {len(words)} words from {self.dictionary_file}")
                return words
        except FileNotFoundError:
            logging.error(f"Dictionary file not found: {self.dictionary_file}")
            return set()
        except Exception as e:
            logging.error(f"Error loading dictionary file: {e}")
            return set()

    def get_all_words(self):
        return self.words