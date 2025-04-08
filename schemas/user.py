from typing import List

from pydantic import BaseModel

from schemas.watched_movie import WatchedMovie


class User(BaseModel):
    id: str
    username: str
    watched_movies: List[WatchedMovie]  # Lista de filmes assistidos

    class Config:
        orm_mode = True