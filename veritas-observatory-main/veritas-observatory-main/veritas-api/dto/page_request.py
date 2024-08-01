from typing import Optional
from pydantic import BaseModel


class PageRequest(BaseModel):
    page: int
    itemsPerPage: Optional[int] = 5
