class ScoreBoard:
    def __init__(self):
        self.score = 0


    def update_score_by_one(self):
        self.score += 1
        print(f"Player score: {self.score}")


    def reduce_score_by_one(self):
        self.score -= 1
        print(f"Player score: {self.score}")

        # Prevent the score from becoming negative
        self.score = 0 if self.score < 0 else self.score

