from pydantic import BaseModel


class SentimentScoreRequest(BaseModel):
    text: str
