from datetime import datetime
from pydantic import BaseModel, Field, validator


class FilterRequest(BaseModel):
    start_date: str = Field(None, description="Start datetime in the format '2021-01-01T00:00:00.000Z'",
                            example="2021-01-03T16:52:05.000Z")
    end_date: str = Field(None, description="End datetime in the format '2021-01-01T00:00:00.000Z'",
                          example="2021-01-03T16:52:05.000Z")
    max_likes: int = Field(None, description="The maximum number of tweet's likes")
    max_followers: int = Field(None, description="The maximum number of user's followers")
    max_retweets: int = Field(None, description="The maximum number of retweets")

    class Config:
        schema_extra = {
            "example": {
                "start_date": "2021-01-01T00:00:00.000Z",
                "end_date": "2021-01-01T00:00:00.000Z",
                "max_likes": 100,
                "max_followers": 1000,
                "max_retweets": 100
            }
        }

    @validator("start_date")
    def validate_datetime_format(cls, value):
        try:
            # Parse the datetime string using strptime with the expected format
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
            return value
        except ValueError:
            raise ValueError("Invalid datetime format")

    @validator("end_date")
    def validate_datetime_format(cls, value):
        try:
            # Parse the datetime string using strptime with the expected format
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
            return value
        except ValueError:
            raise ValueError("Invalid datetime format")
