from typing import List

from database import db
from schemas.movie import Movie


class MovieRepository:
    @staticmethod
    def get_movies(skip: int, filter_query: dict, limit: int) -> List[Movie]:
        return list(db.titles.find(filter_query).skip(skip).limit(limit))

    @staticmethod
    def get_ratings(limit: int) -> list:
        return list(db.ratings.find({"averageRating": {"$exists": True}}).sort("averageRating", -1).limit(limit))

    @staticmethod
    def find_one_title(tconst: str):
        return db.titles.find_one({"tconst": tconst})

    @staticmethod
    def find_crew_by_high_rated(high_rated: List[str]) -> list:
        return db.crew.find({"tconst": {"$in": high_rated}}, {"directors": 1})

    @staticmethod
    def filter_crew_by_directors(regex: str, watched_tconsts: List[dict], limit: int) -> list:
        return db.crew.find({"directors": {"$regex": regex, "$options": "i"},
                             "tconst": {"$nin": watched_tconsts}}).limit(limit).sort("tconst", -1)

    @staticmethod
    def find_actors(high_rated: List[str], limit: int = 2) -> list:
        return db.principals.find({"tconst": {"$in": high_rated}, "category": "actor"},
                                  {"nconst": 1}).limit(limit)

    @staticmethod
    def filter_actors(actor: str, length: int, limit: int) -> list:
        return db.principals.find({"nconst": actor}, {"tconst": 1}).sort("tconst", -1).limit(limit - length)

    @staticmethod
    def filter_movies(rec: List[str], limit: int) -> List[Movie]:
        return list(db.titles.find({"tconst": {"$in": rec}}).limit(limit))

    @staticmethod
    def filter_movies_by_genre(genre: str, watched_tconsts: List[dict], limit: int) -> List[Movie]:
        return list(db.titles.find({"genres": {"$regex": genre, "$options": "i"}, "tconst": {"$nin": watched_tconsts},
                                    "titleType": {"$in": ["movie", "tvSeries"]}
                                    }).sort("tconst", -1).limit(limit)
                    )

    @staticmethod
    def filter_movies_by_tconst(watched_tconsts: List[str]) -> List[Movie]:
        return list(db.titles.find({"tconst": {"$in": watched_tconsts}}, {"tconst": 1, "genres": 1}))