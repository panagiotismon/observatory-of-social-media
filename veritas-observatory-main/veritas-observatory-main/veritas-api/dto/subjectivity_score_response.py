class SubjectivityScoreResponse:

    def __init__(self, text, score):
        self._text: str = text
        self._score: float = score

    def get_text(self):
        return self._text

    def get_score(self):
        return self._score
