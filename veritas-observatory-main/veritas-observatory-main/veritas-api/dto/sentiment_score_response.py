from pydantic import BaseModel


class SentimentScoreResponse(BaseModel):
    text: str
    label: str
    class Config:
        orm_mode = True