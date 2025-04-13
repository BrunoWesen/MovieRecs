from typing import List

from bson import ObjectId

from app.database import db
from app.schemas.user import UserResponse
from app.schemas.watched_movie import WatchedMovie


class UserRepository:
    @staticmethod
    def get_users(skip: int, filter_query: dict, limit: int) -> List[UserResponse]:
        return list(db.users.find(filter_query).skip(skip).limit(limit))

    @staticmethod
    def find_user_by_id(id: ObjectId) -> UserResponse:
        user = db.users.find_one({"_id": id})
        user["_id"] = str(user["_id"])
        return user

    @staticmethod
    def insert_one_user(user_data: dict):
        return db.users.insert_one(user_data)

    @staticmethod
    def update_watched_movie(id: ObjectId, movie: WatchedMovie):
        return db.users.update_one({"_id": id, "watched_movies.tconst": movie.tconst},
                                   {"$set": {"watched_movies.$.rating": movie.rating}})

    @staticmethod
    def insert_watched_movie(id: ObjectId, movie: WatchedMovie):
        return db.users.update_one({"_id": id},{"$push": {"watched_movies": movie.model_dump()}})
