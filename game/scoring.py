class ScoringSystem:
    def __init__(self):
        self.score = 0
        self.word_count = 0

    def update_score(self, words_transformed):
        """Update the score based on the number of words transformed."""
        self.word_count += words_transformed
        self.score += words_transformed * 10  # Each word transformed gives 10 points

    def get_score(self):
        """Return the current score."""
        return self.score

    def reset_score(self):
        """Reset the score and word count for a new game."""
        self.score = 0
        self.word_count = 0

    def calculate_bonus(self):
        """Calculate bonus points based on performance."""
        if self.word_count >= 5:
            return 50  # Bonus for transforming 5 or more words
        return 0

    def finalize_score(self):
        """Finalize the score at the end of the game."""
        bonus = self.calculate_bonus()
        self.score += bonus
        return self.score