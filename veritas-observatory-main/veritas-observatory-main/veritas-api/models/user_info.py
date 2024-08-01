from pydantic import BaseModel


class UserInformation(BaseModel):

    user_id: int
    user_followers_count: int
    user_tweet_count: int
