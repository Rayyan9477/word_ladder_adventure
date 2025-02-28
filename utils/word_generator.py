import random

class RandomWordGenerator:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.word_lengths = {3: [], 4: [], 5: [], 6: [], 7: []}
        self._categorize_words()
        
    def _categorize_words(self):
        """Categorize words by length for faster retrieval"""
        for word in self.dictionary:
            length = len(word)
            if 3 <= length <= 7:  # Only consider words between 3-7 characters
                if word not in self.word_lengths[length]:
                    self.word_lengths[length].append(word)

    def get_random_pair(self, difficulty="medium"):
        """Get a random pair of words based on difficulty level
        
        difficulty: "easy" (3-4 letters), "medium" (5 letters), "hard" (6-7 letters)
        """
        if difficulty == "easy":
            lengths = [3, 4]
        elif difficulty == "medium":
            lengths = [5]
        else:  # hard
            lengths = [6, 7]
            
        length = random.choice(lengths)
        words = self.word_lengths[length]
        
        if len(words) < 2:
            return None, None
            
        # Try to find word pairs that have a valid path
        for _ in range(10):  # Try 10 times
            start_word = random.choice(words)
            end_word = random.choice(words)
            
            # Ensure words are different but don't check path here
            # Path validation will be done in game logic
            if start_word != end_word:
                return start_word, end_word
                
        # Fallback
        return words[0], words[-1]