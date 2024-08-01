from typing import Any

from pydantic import BaseModel

from models.location_info import LocationInformation
from models.tweet_metrics import TweetMetrics
from models.user_info import UserInformation


class TweetSample(BaseModel):
    created_at: str
    tweet_id: int
    text: str
    hashtags: list
    url: str | None
    user_info: UserInformation
    location_info: LocationInformation
    tweet_metrics: TweetMetrics
    tweet_trust_score: int
    sentiment_score: int
    subjectivity_label: float

    def to_dict(self):
        user_info_dict = self.user_info.__dict__
        location_info_dict = self.location_info.__dict__
        tweet_metrics_dict = self.tweet_metrics.__dict__
        tweet_sample_dict = self.__dict__
        tweet_sample_dict["user_info"] = user_info_dict
        tweet_sample_dict["location_info"] = location_info_dict
        tweet_sample_dict["tweet_metrics"] = tweet_metrics_dict

        return tweet_sample_dict

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

