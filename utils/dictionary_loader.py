import os

class DictionaryLoader:
    def __init__(self, dictionary_file='data/dictionary.txt'):
        self.dictionary_file = dictionary_file
        self.words = self.load_dictionary()

    def load_dictionary(self):
        if not os.path.exists(self.dictionary_file):
            raise FileNotFoundError(f"Dictionary file not found: {self.dictionary_file}")
        
        with open(self.dictionary_file, 'r') as file:
            words = {line.strip().lower() for line in file if line.strip()}
        return words

    def is_valid_word(self, word):
        return word.lower() in self.words

    def get_all_words(self):
        return self.words

# Example usage:
# loader = DictionaryLoader()
# print(loader.get_all_words())  # This will print all valid words from the dictionary.