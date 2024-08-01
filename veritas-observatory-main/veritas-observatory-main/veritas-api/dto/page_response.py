from charset_normalizer.md import List
from pydantic import BaseModel

from models.tweet_sample import TweetSample


class PageResponse(BaseModel):
    data: List[TweetSample]
    page: int
    total_pages: int
    class Config:
        orm_mode = True
