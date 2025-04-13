from typing import Optional

from pydantic import BaseModel


class WatchedMovie(BaseModel):
    tconst: str
    rating: Optional[float] = None  # Pode ser None se o usuário não avaliou
