class ScoringSystem:
    def __init__(self):
        self.score = 0
        self.word_count = 0

    def update_score(self, words_transformed):
        self.word_count += words_transformed
        self.score += words_transformed * 10  # Each word transformed gives 10 points

    def get_score(self):
        return self.score

    def reset_score(self):
        self.score = 0
        self.word_count = 0

    def calculate_bonus(self):
        if self.word_count >= 5:
            return 50  
        return 0

    def finalize_score(self):
        bonus = self.calculate_bonus()
        self.score += bonus
        return self.score