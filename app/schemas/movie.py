from pydantic import BaseModel
from typing import Optional


class Movie(BaseModel):
    tconst: str
    titleType: str
    primaryTitle: str
    originalTitle: str
    isAdult: Optional[int]
    startYear: Optional[int]
    endYear: Optional[int]
    runtimeMinutes: Optional[int]
    genres: Optional[str]

    model_config = {
        "from_attributes": True
    }