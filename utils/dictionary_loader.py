class DictionaryLoader:
    def __init__(self, dictionary_file):
        self.dictionary_file = dictionary_file
        self.words = self.load_dictionary()
        
    def load_dictionary(self):
        try:
            with open(self.dictionary_file, 'r') as f:
                return {word.strip().upper() for word in f if word.strip()}
        except FileNotFoundError:
            raise FileNotFoundError(f"Dictionary file not found: {self.dictionary_file}")
            
    def get_all_words(self):
        return self.words