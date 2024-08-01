from pydantic import BaseModel


class LocationInformation(BaseModel):

    location: str | None
    country: str | None
    state: str | None
