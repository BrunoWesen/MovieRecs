from typing import List

from pydantic import BaseModel, Field

from app.schemas.watched_movie import WatchedMovie


class UserCreate(BaseModel):
    username: str
    watched_movies: List[WatchedMovie]


class UserResponse(BaseModel):
    id: str = Field(..., alias="_id")
    username: str
    watched_movies: List[WatchedMovie]

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
