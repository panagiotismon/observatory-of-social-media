from pydantic import BaseModel


class TweetMetrics(BaseModel):
    retweets_count: int
    likes_count: int
    replies_count: int
