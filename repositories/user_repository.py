from database import db
from schemas.watched_movie import WatchedMovie


class UserRepository:
    @staticmethod
    def find_user_by_id(id: str):
        return db.users.find_one({"id": id})

    @staticmethod
    def insert_one_user(user_data: dict):
        return db.users.insert_one(user_data)

    @staticmethod
    def update_watched_movie(id: str, movie: WatchedMovie):
        return db.users.update_one({"id": id, "watched_movies.tconst": movie.tconst},
                                   {"$set": {"watched_movies.$.rating": movie.rating}})

    @staticmethod
    def insert_watched_movie(id: str, movie: WatchedMovie):
        return db.users.update_one({"id": id},{"$push": {"watched_movies": movie.model_dump()}})
