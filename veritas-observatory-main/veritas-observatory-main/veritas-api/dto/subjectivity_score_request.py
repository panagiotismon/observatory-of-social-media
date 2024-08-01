from pydantic import BaseModel


class SubjectivityScoreRequest(BaseModel):
    text: str
